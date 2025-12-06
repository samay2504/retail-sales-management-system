"""Test configuration and fixtures."""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.models.base import Base
from src.models.transaction import Transaction


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        yield session

    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def sample_transactions(db_session: AsyncSession) -> list[Transaction]:
    """Create sample transactions for testing."""
    from datetime import date

    transactions = [
        Transaction(
            transaction_id=1,
            customer_id="CUST-00001",
            customer_name="John Smith",
            phone_number="+1-555-0001",
            customer_region="North",
            customer_type="New",
            gender="Male",
            age=35,
            date=date(2024, 1, 15),
            product_id="PROD-0001",
            product_name="Laptop",
            brand="Dell",
            product_category="Electronics",
            tags="bestseller, premium",
            quantity=2,
            price_per_unit=100.0,
            discount_percentage=10.0,
            total_amount=200.0,
            final_amount=180.0,
            payment_method="Credit Card",
            order_status="Completed",
            delivery_type="Standard",
            store_id="STORE-1001",
            store_location="New York, NY",
            salesperson_id="EMP-101",
            employee_name="Alice Johnson",
        ),
        Transaction(
            transaction_id=2,
            customer_id="CUST-00002",
            customer_name="Jane Doe",
            phone_number="+1-555-0002",
            customer_region="South",
            customer_type="Returning",
            gender="Female",
            age=28,
            date=date(2024, 1, 16),
            product_id="PROD-0002",
            product_name="T-Shirt",
            brand="Nike",
            product_category="Clothing",
            tags="new-arrival",
            quantity=1,
            price_per_unit=50.0,
            discount_percentage=0.0,
            total_amount=50.0,
            final_amount=50.0,
            payment_method="Cash",
            order_status="Pending",
            delivery_type="Express",
            store_id="STORE-1002",
            store_location="Los Angeles, CA",
            salesperson_id="EMP-102",
            employee_name="Bob Smith",
        ),
        Transaction(
            transaction_id=3,
            customer_id="CUST-00003",
            customer_name="Bob Johnson",
            phone_number="+1-555-0003",
            customer_region="East",
            customer_type="Loyal",
            gender="Male",
            age=42,
            date=date(2024, 1, 17),
            product_id="PROD-0003",
            product_name="Apple",
            brand="Organic Farms",
            product_category="Food & Beverage",
            tags="clearance, sale",
            quantity=5,
            price_per_unit=20.0,
            discount_percentage=15.0,
            total_amount=100.0,
            final_amount=85.0,
            payment_method="Debit Card",
            order_status="Cancelled",
            delivery_type="Store Pickup",
            store_id="STORE-1003",
            store_location="Chicago, IL",
            salesperson_id="EMP-103",
            employee_name="Carol Davis",
        ),
    ]

    db_session.add_all(transactions)
    await db_session.commit()

    # Refresh to get IDs
    for transaction in transactions:
        await db_session.refresh(transaction)

    # Create FTS table for testing
    await db_session.execute(
        text(
            """
        CREATE VIRTUAL TABLE IF NOT EXISTS transactions_fts USING fts5(
            customer_name,
            phone_number,
            content='transactions',
            content_rowid='id'
        )
    """
        )
    )

    await db_session.execute(
        text(
            """
        INSERT INTO transactions_fts(rowid, customer_name, phone_number)
        SELECT id, customer_name, phone_number FROM transactions
    """
        )
    )

    await db_session.commit()

    return transactions
