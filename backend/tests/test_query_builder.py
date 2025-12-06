"""Tests for QueryBuilder service."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.transaction import Transaction
from src.services.query_builder import QueryBuilder
from src.schemas.transaction import TransactionListQuery


@pytest.mark.asyncio
async def test_query_builder_basic_list(db_session: AsyncSession, sample_transactions):
    """Test basic transaction listing."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert len(transactions) == 3
    assert total == 3
    assert all(isinstance(t, Transaction) for t in transactions)


@pytest.mark.asyncio
async def test_query_builder_search_customer_name(db_session: AsyncSession, sample_transactions):
    """Test search by customer name."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(q="John", page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 1  # Only "John Smith" (FTS matches whole words)
    assert "john" in transactions[0].customer_name.lower()


@pytest.mark.asyncio
async def test_query_builder_search_phone(db_session: AsyncSession, sample_transactions):
    """Test search by phone number."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(q="555-0001", page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 1
    assert transactions[0].phone_number == "+1-555-0001"


@pytest.mark.asyncio
async def test_query_builder_filter_region(db_session: AsyncSession, sample_transactions):
    """Test filter by region."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(customer_region=["North"], page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 1
    assert transactions[0].customer_region == "North"


@pytest.mark.asyncio
async def test_query_builder_filter_multiple_regions(db_session: AsyncSession, sample_transactions):
    """Test filter by multiple regions."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(customer_region=["North", "South"], page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 2
    assert all(t.customer_region in ["North", "South"] for t in transactions)


@pytest.mark.asyncio
async def test_query_builder_filter_age_range(db_session: AsyncSession, sample_transactions):
    """Test filter by age range."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(age_min=30, age_max=40, page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 1
    assert 30 <= transactions[0].age <= 40


@pytest.mark.asyncio
async def test_query_builder_sort_by_date_desc(db_session: AsyncSession, sample_transactions):
    """Test sorting by date descending."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(sort="date:desc", page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 3
    # Check dates are in descending order
    dates = [t.date for t in transactions]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.asyncio
async def test_query_builder_sort_by_quantity_asc(db_session: AsyncSession, sample_transactions):
    """Test sorting by quantity ascending."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(sort="quantity:asc", page=1, limit=10)
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 3
    # Check quantities are in ascending order
    quantities = [t.quantity for t in transactions]
    assert quantities == sorted(quantities)


@pytest.mark.asyncio
async def test_query_builder_pagination(db_session: AsyncSession, sample_transactions):
    """Test pagination."""
    builder = QueryBuilder(db_session)
    
    # Page 1 with limit 2
    params = TransactionListQuery(page=1, limit=2, sort="date:asc")
    transactions, total = await builder.build_list_query(params)
    
    assert len(transactions) == 2
    assert total == 3
    first_page_ids = [t.id for t in transactions]
    
    # Page 2 with limit 2
    params = TransactionListQuery(page=2, limit=2, sort="date:asc")
    transactions, total = await builder.build_list_query(params)
    
    assert len(transactions) == 1
    assert total == 3
    second_page_ids = [t.id for t in transactions]
    
    # Ensure no overlap
    assert not set(first_page_ids).intersection(second_page_ids)


@pytest.mark.asyncio
async def test_query_builder_combined_search_and_filter(db_session: AsyncSession, sample_transactions):
    """Test combining search and filters."""
    builder = QueryBuilder(db_session)
    params = TransactionListQuery(
        q="John",
        customer_region=["North"],
        page=1,
        limit=10
    )
    
    transactions, total = await builder.build_list_query(params)
    
    assert total == 1
    assert "john" in transactions[0].customer_name.lower()
    assert transactions[0].customer_region == "North"


@pytest.mark.asyncio
async def test_query_builder_get_filter_metadata(db_session: AsyncSession, sample_transactions):
    """Test getting filter metadata."""
    builder = QueryBuilder(db_session)
    metadata = await builder.get_filter_metadata()
    
    assert "customer_regions" in metadata
    assert "genders" in metadata
    assert "product_categories" in metadata
    assert "tags" in metadata
    assert "payment_methods" in metadata
    assert "age_range" in metadata
    assert "date_range" in metadata
    
    # Check regions
    regions = [opt["value"] for opt in metadata["customer_regions"]]
    assert "North" in regions
    assert "South" in regions
    assert "East" in regions
    
    # Check age range
    assert metadata["age_range"]["min"] == 28
    assert metadata["age_range"]["max"] == 42
