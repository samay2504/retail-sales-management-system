"""Tests for TransactionService."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.transaction_service import TransactionService
from src.schemas.transaction import TransactionListQuery


@pytest.mark.asyncio
async def test_transaction_service_list(db_session: AsyncSession, sample_transactions):
    """Test listing transactions."""
    service = TransactionService(db_session)
    params = TransactionListQuery(page=1, limit=10)

    result = await service.list_transactions(params)

    assert "items" in result
    assert "meta" in result
    assert len(result["items"]) == 3
    assert result["meta"].total == 3


@pytest.mark.asyncio
async def test_transaction_service_get_by_id(db_session: AsyncSession, sample_transactions):
    """Test getting transaction by ID."""
    service = TransactionService(db_session)
    transaction_id = sample_transactions[0].id

    transaction = await service.get_transaction_by_id(transaction_id)

    assert transaction is not None
    assert transaction.id == transaction_id
    assert transaction.customer_name == "John Smith"


@pytest.mark.asyncio
async def test_transaction_service_get_nonexistent(db_session: AsyncSession, sample_transactions):
    """Test getting nonexistent transaction."""
    service = TransactionService(db_session)

    transaction = await service.get_transaction_by_id(99999)

    assert transaction is None


@pytest.mark.asyncio
async def test_transaction_service_filter_metadata(db_session: AsyncSession, sample_transactions):
    """Test getting filter metadata."""
    service = TransactionService(db_session)

    metadata = await service.get_filter_metadata()

    assert "customer_regions" in metadata
    assert len(metadata["customer_regions"]) > 0
    assert all("value" in opt and "count" in opt for opt in metadata["customer_regions"])
