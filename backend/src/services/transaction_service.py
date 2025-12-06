"""Transaction service for business logic."""

from typing import Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.transaction import Transaction
from src.schemas.transaction import TransactionListQuery, TransactionResponse, PaginationMeta
from src.services.query_builder import QueryBuilder
from src.utils.cache import cache_manager
from src.utils.logging import get_logger

logger = get_logger(__name__)


class TransactionService:
    """Service for transaction operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.query_builder = QueryBuilder(session)

    async def get_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        """Get a single transaction by ID."""
        query = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_transactions(self, params: TransactionListQuery) -> Dict[str, Any]:
        """List transactions with search, filters, sorting, and pagination."""
        # Generate cache key
        cache_key = cache_manager.generate_cache_key(
            "transactions_list",
            q=params.q,
            page=params.page,
            limit=params.limit,
            sort=params.sort,
            customer_region=params.customer_region,
            gender=params.gender,
            product_category=params.product_category,
            tags=params.tags,
            payment_method=params.payment_method,
            age_min=params.age_min,
            age_max=params.age_max,
            date_from=params.date_from,
            date_to=params.date_to,
        )

        # Check cache
        cached = await cache_manager.get(cache_key)
        if cached:
            logger.info(f"Returning cached result for query: {params.q or 'no search'}")
            return cached

        # Build and execute query
        transactions, total_count = await self.query_builder.build_list_query(params)

        # Calculate pagination metadata
        total_pages = (total_count + params.limit - 1) // params.limit
        has_next = params.page < total_pages
        has_prev = params.page > 1

        # Build response
        response = {
            "items": [TransactionResponse.model_validate(t.to_dict()) for t in transactions],
            "meta": PaginationMeta(
                total=total_count,
                page=params.page,
                limit=params.limit,
                total_pages=total_pages,
                has_next=has_next,
                has_prev=has_prev,
            ),
        }

        # Cache response
        await cache_manager.set(cache_key, response)

        return response

    async def get_filter_metadata(self) -> Dict[str, Any]:
        """Get filter metadata (unique values and counts)."""
        # Generate cache key
        cache_key = cache_manager.generate_cache_key("filter_metadata")

        # Check cache
        cached = await cache_manager.get(cache_key)
        if cached:
            logger.info("Returning cached filter metadata")
            return cached

        # Get metadata
        metadata = await self.query_builder.get_filter_metadata()

        # Cache metadata (longer TTL)
        await cache_manager.set(cache_key, metadata, ttl=300)  # 5 minutes

        return metadata

    async def create_transaction(self, transaction_data: Dict[str, Any]) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(**transaction_data)
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        # Invalidate caches
        await cache_manager.clear()

        logger.info(f"Created transaction: {transaction.id}")
        return transaction
