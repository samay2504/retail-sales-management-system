"""
Migration script from SQLite to PostgreSQL for production.
Converts FTS5 (SQLite) to PostgreSQL full-text search with tsvector.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.transaction import Transaction


async def create_postgres_schema(database_url: str):
    """Create tables and indexes in PostgreSQL."""
    print("🔧 Creating PostgreSQL schema...")

    # Convert to async URL if needed
    if not database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        # Drop all tables if they exist
        await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

        # Add full-text search (PostgreSQL tsvector)
        await conn.execute(
            text(
                """
            -- Add tsvector column for full-text search
            ALTER TABLE transactions 
            ADD COLUMN IF NOT EXISTS search_vector tsvector;
        """
            )
        )

        await conn.execute(
            text(
                """
            -- Create GIN index for full-text search
            CREATE INDEX IF NOT EXISTS idx_transactions_search 
            ON transactions USING GIN(search_vector);
        """
            )
        )

        # Split trigger creation into separate commands for asyncpg
        await conn.execute(
            text(
                """
            CREATE OR REPLACE FUNCTION transactions_search_trigger() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector :=
                    setweight(to_tsvector('english', COALESCE(NEW.customer_name, '')), 'A') ||
                    setweight(to_tsvector('english', COALESCE(NEW.phone_number, '')), 'B');
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """
            )
        )

        await conn.execute(text("DROP TRIGGER IF EXISTS tsvector_update_trigger ON transactions;"))

        await conn.execute(
            text(
                """
            CREATE TRIGGER tsvector_update_trigger
            BEFORE INSERT OR UPDATE ON transactions
            FOR EACH ROW EXECUTE FUNCTION transactions_search_trigger();
        """
            )
        )

        print("✅ PostgreSQL schema created successfully!")

    await engine.dispose()


async def seed_postgres(database_url: str, num_records: int = 1000):
    """Seed PostgreSQL database with sample data."""
    print(f"🌱 Seeding database with {num_records} records...")

    if not database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

    engine = create_async_engine(database_url, echo=False)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Import seed function from seed_db
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from seed_db import generate_transaction

    async with async_session_maker() as session:
        # Generate transactions
        transactions_data = [generate_transaction() for _ in range(num_records)]

        # Convert to Transaction models
        transactions = [Transaction(**data) for data in transactions_data]

        # Batch insert
        batch_size = 100
        for i in range(0, len(transactions), batch_size):
            batch = transactions[i : i + batch_size]
            session.add_all(batch)
            await session.commit()
            print(
                f"  Inserted {min(i + batch_size, len(transactions))}/{len(transactions)} records"
            )

        # Verify count
        result = await session.execute(text("SELECT COUNT(*) FROM transactions"))
        count = result.scalar()
        print(f"✅ Database seeded! Total records: {count}")

    await engine.dispose()


async def main():
    """Main migration function."""
    print("🚀 PostgreSQL Production Migration")
    print("=" * 50)

    # Get DATABASE_URL from environment or prompt
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("\n❌ DATABASE_URL not found in environment!")
        print("\nPlease set it first:")
        print("  $env:DATABASE_URL='postgresql://user:pass@host:5432/truestate_prod'")
        print("  python scripts/migrate_to_postgres.py")
        sys.exit(1)

    print(
        f"\n📊 Target Database: {database_url.split('@')[1] if '@' in database_url else 'localhost'}"
    )

    # Ask for confirmation
    response = input(
        "\n⚠️  This will DROP all existing tables and recreate them. Continue? (yes/no): "
    )
    if response.lower() != "yes":
        print("❌ Migration cancelled.")
        sys.exit(0)

    try:
        # Step 1: Create schema
        await create_postgres_schema(database_url)

        # Step 2: Seed data
        num_records = int(input("\nHow many records to seed? (default 1000): ") or "1000")
        await seed_postgres(database_url, num_records)

        print("\n✅ Migration completed successfully!")
        print("\n📝 Next steps:")
        print("1. Update backend/.env with:")
        print(f"   DATABASE_URL={database_url}")
        print("2. Test locally: python -m uvicorn src.index:app --reload")
        print("3. Deploy to Render with the DATABASE_URL from Render dashboard")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
