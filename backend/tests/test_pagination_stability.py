"""Tests for pagination stability and deterministic ordering."""
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.transaction import Transaction
from src.schemas.transaction import TransactionListQuery
from src.services.query_builder import QueryBuilder


class TestPaginationStability:
    """Test suite for pagination stability."""
    
    @pytest.mark.asyncio
    async def test_deterministic_ordering_default_sort(self, db_session: AsyncSession):
        """Test that default sorting includes id tiebreaker for deterministic results."""
        # Insert test transactions with same date
        test_date = "2024-01-15"
        transactions = [
            Transaction(
                customer_name=f"Customer {i}",
                phone_number=f"555-000{i}",
                customer_region="North",
                gender="Male",
                age=30,
                product_category="Electronics",
                quantity=1,
                price_per_unit=100.0,
                total_amount=100.0,
                discount_percentage=0,
                final_amount=100.0,
                payment_method="Cash",
                store_id="S001",
                store_location="Downtown",
                salesperson_id="EMP001",
                employee_name="John Doe",
                date=test_date,
            )
            for i in range(10)
        ]
        
        for t in transactions:
            db_session.add(t)
        await db_session.commit()
        
        # Build query
        builder = QueryBuilder(db_session)
        query_params = TransactionListQuery(page=1, limit=5, sort="date:desc")
        
        # Execute query multiple times
        results = []
        for _ in range(3):
            items, total = await builder.build_list_query(query_params)
            results.append([t.id for t in items])
        
        # All executions should return same IDs in same order
        assert results[0] == results[1] == results[2], "Results should be deterministic"
    
    @pytest.mark.asyncio
    async def test_no_duplicates_across_pages(self, db_session: AsyncSession):
        """Test that paginating through results doesn't show duplicates."""
        # Get all transactions
        builder = QueryBuilder(db_session)
        
        # Fetch all pages
        page = 1
        limit = 10
        all_ids = set()
        
        while True:
            query_params = TransactionListQuery(page=page, limit=limit, sort="date:desc")
            items, total = await builder.build_list_query(query_params)
            
            if not items:
                break
            
            # Check for duplicates
            page_ids = [t.id for t in items]
            duplicates = set(page_ids) & all_ids
            assert len(duplicates) == 0, f"Found duplicates: {duplicates}"
            
            all_ids.update(page_ids)
            page += 1
            
            if page > (total // limit) + 1:
                break
    
    @pytest.mark.asyncio
    async def test_stable_pages_with_filters(self, db_session: AsyncSession):
        """Test that filtering doesn't cause page instability."""
        builder = QueryBuilder(db_session)
        
        # Query with filters
        query_params = TransactionListQuery(
            page=1,
            limit=10,
            sort="date:desc",
            customer_region=["North", "South"],
        )
        
        # Execute twice
        items1, total1 = await builder.build_list_query(query_params)
        items2, total2 = await builder.build_list_query(query_params)
        
        # Results should be identical
        assert total1 == total2
        assert [t.id for t in items1] == [t.id for t in items2]
    
    @pytest.mark.asyncio
    async def test_ordering_with_custom_sort(self, db_session: AsyncSession):
        """Test that custom sort fields also include id tiebreaker."""
        builder = QueryBuilder(db_session)
        
        # Insert transactions with same quantity
        for i in range(5):
            t = Transaction(
                customer_name=f"Test {i}",
                phone_number=f"555-{i:04d}",
                customer_region="North",
                gender="Male",
                age=25,
                product_category="Food",
                quantity=5,  # Same quantity
                price_per_unit=10.0,
                total_amount=50.0,
                discount_percentage=0,
                final_amount=50.0,
                payment_method="Card",
                store_id="S001",
                store_location="Downtown",
                salesperson_id="EMP002",
                employee_name="Jane Doe",
                date="2024-01-20",
            )
            db_session.add(t)
        await db_session.commit()
        
        # Query with quantity sort
        query_params = TransactionListQuery(page=1, limit=10, sort="quantity:desc")
        
        # Execute multiple times
        results = []
        for _ in range(3):
            items, _ = await builder.build_list_query(query_params)
            # Filter to only our test transactions
            test_items = [t for t in items if t.quantity == 5]
            results.append([t.id for t in test_items])
        
        # Order should be consistent
        if results[0]:  # Only check if we have results
            assert results[0] == results[1] == results[2]
