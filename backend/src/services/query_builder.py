"""Query builder for transactions with search, filters, sorting, and pagination."""
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.models.transaction import Transaction
from src.schemas.transaction import TransactionListQuery
from src.utils.logging import get_logger

logger = get_logger(__name__)


class QueryBuilder:
    """Build complex queries for transaction search, filter, sort, and pagination."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _normalize_search_query(self, query: str) -> str:
        """Normalize search query for FTS matching."""
        # Remove extra whitespace and normalize
        normalized = " ".join(query.strip().lower().split())
        
        # If query contains special characters like hyphens, quote it for FTS5
        if "-" in normalized or "." in normalized or "+" in normalized:
            normalized = f'"{normalized}"'
        
        return normalized
    
    async def _ensure_fts_table(self) -> None:
        """Ensure FTS5 virtual table exists."""
        # Check if FTS table exists
        check_query = text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='transactions_fts'
        """)
        result = await self.session.execute(check_query)
        exists = result.scalar() is not None
        
        if not exists:
            logger.info("Creating FTS5 virtual table")
            # Create FTS5 virtual table
            create_fts = text("""
                CREATE VIRTUAL TABLE transactions_fts USING fts5(
                    customer_name,
                    phone_number,
                    content='transactions',
                    content_rowid='id'
                )
            """)
            await self.session.execute(create_fts)
            
            # Populate FTS table
            populate_fts = text("""
                INSERT INTO transactions_fts(rowid, customer_name, phone_number)
                SELECT id, customer_name, phone_number FROM transactions
            """)
            await self.session.execute(populate_fts)
            await self.session.commit()
            logger.info("FTS5 table created and populated")
    
    def _build_base_query(self) -> Select:
        """Build base SELECT query."""
        return select(Transaction)
    
    def _apply_search(self, query: Select, search_term: str) -> Tuple[Select, bool]:
        """Apply full-text search using FTS5."""
        if not search_term:
            return query, False
        
        normalized = self._normalize_search_query(search_term)
        
        # Use FTS5 MATCH for full-text search
        # Join with FTS table and filter by match
        fts_subquery = text("""
            SELECT rowid as id FROM transactions_fts 
            WHERE transactions_fts MATCH :search_term
        """)
        
        # Add join condition
        query = query.where(
            Transaction.id.in_(
                select(text("id")).select_from(text(f"({fts_subquery.text})")).params(search_term=normalized)
            )
        )
        
        return query, True
    
    def _apply_filters(self, query: Select, params: TransactionListQuery) -> Select:
        """Apply filter conditions."""
        conditions = []
        
        # Multi-select filters
        if params.customer_region:
            conditions.append(Transaction.customer_region.in_(params.customer_region))
        
        if params.gender:
            conditions.append(Transaction.gender.in_(params.gender))
        
        if params.product_category:
            conditions.append(Transaction.product_category.in_(params.product_category))
        
        if params.payment_method:
            conditions.append(Transaction.payment_method.in_(params.payment_method))
        
        # Tags filter (contains any of the specified tags)
        if params.tags:
            tag_conditions = []
            for tag in params.tags:
                tag_conditions.append(Transaction.tags.like(f"%{tag}%"))
            conditions.append(or_(*tag_conditions))
        
        # Range filters
        if params.age_min is not None:
            conditions.append(Transaction.age >= params.age_min)
        
        if params.age_max is not None:
            conditions.append(Transaction.age <= params.age_max)
        
        if params.date_from:
            conditions.append(Transaction.date >= params.date_from)
        
        if params.date_to:
            conditions.append(Transaction.date <= params.date_to)
        
        # Apply all conditions
        if conditions:
            query = query.where(and_(*conditions))
        
        return query
    
    def _apply_sorting(
        self, query: Select, sort_param: Optional[str], has_search: bool
    ) -> Select:
        """Apply sorting with deterministic tiebreaker."""
        if not sort_param:
            # Default sort: date DESC, id DESC for deterministic pagination
            return query.order_by(Transaction.date.desc(), Transaction.id.desc())
        
        field, direction = sort_param.split(":")
        
        # Map field names to columns
        field_map = {
            "date": Transaction.date,
            "quantity": Transaction.quantity,
            "customer_name": Transaction.customer_name,
        }
        
        column = field_map.get(field, Transaction.date)
        
        # Always add id as tiebreaker for deterministic ordering
        if direction == "desc":
            query = query.order_by(column.desc(), Transaction.id.desc())
        else:
            query = query.order_by(column.asc(), Transaction.id.asc())
        
        return query
    
    def _apply_pagination(
        self, query: Select, page: int, limit: int
    ) -> Select:
        """Apply pagination with limit and offset."""
        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)
        return query
    
    async def build_list_query(
        self, params: TransactionListQuery
    ) -> Tuple[List[Transaction], int]:
        """Build and execute query for transaction list with count."""
        # Ensure FTS table exists
        await self._ensure_fts_table()
        
        # Build base query
        query = self._build_base_query()
        
        # Apply search
        has_search = False
        if params.q:
            query, has_search = self._apply_search(query, params.q)
        
        # Apply filters
        query = self._apply_filters(query, params)
        
        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar() or 0
        
        # Apply sorting
        query = self._apply_sorting(query, params.sort, has_search)
        
        # Apply pagination
        query = self._apply_pagination(query, params.page, params.limit)
        
        # Execute query
        result = await self.session.execute(query)
        transactions = result.scalars().all()
        
        logger.info(
            f"Query executed: search={params.q}, filters={len([f for f in [params.customer_region, params.gender, params.product_category] if f])}, "
            f"sort={params.sort}, page={params.page}, results={len(transactions)}/{total_count}"
        )
        
        return list(transactions), total_count
    
    async def get_filter_metadata(self) -> Dict[str, Any]:
        """Get unique values and counts for filter fields."""
        metadata: Dict[str, Any] = {
            "customer_regions": [],
            "genders": [],
            "product_categories": [],
            "tags": [],
            "payment_methods": [],
            "age_range": {"min": 0, "max": 100},
            "date_range": {"min": None, "max": None},
        }
        
        # Get unique values with counts for categorical fields
        for field_name, model_field in [
            ("customer_regions", Transaction.customer_region),
            ("genders", Transaction.gender),
            ("product_categories", Transaction.product_category),
            ("payment_methods", Transaction.payment_method),
        ]:
            query = select(model_field, func.count(Transaction.id)).group_by(model_field).order_by(func.count(Transaction.id).desc())
            result = await self.session.execute(query)
            rows = result.all()
            metadata[field_name] = [{"value": row[0], "count": row[1]} for row in rows]
        
        # Get unique tags (split comma-separated tags)
        query = select(Transaction.tags).where(Transaction.tags.isnot(None))
        result = await self.session.execute(query)
        all_tags: Dict[str, int] = {}
        for row in result.scalars():
            if row:
                tags = [tag.strip() for tag in row.split(",")]
                for tag in tags:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
        
        metadata["tags"] = [
            {"value": tag, "count": count}
            for tag, count in sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Get age range
        age_query = select(func.min(Transaction.age), func.max(Transaction.age))
        age_result = await self.session.execute(age_query)
        age_row = age_result.one()
        metadata["age_range"] = {"min": age_row[0] or 0, "max": age_row[1] or 100}
        
        # Get date range
        date_query = select(func.min(Transaction.date), func.max(Transaction.date))
        date_result = await self.session.execute(date_query)
        date_row = date_result.one()
        metadata["date_range"] = {"min": date_row[0], "max": date_row[1]}
        
        return metadata
