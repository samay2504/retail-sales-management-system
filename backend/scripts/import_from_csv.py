"""Import 1M records from CSV file into PostgreSQL database."""

import asyncio
import csv
import os
from datetime import datetime
from typing import List, Dict

import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CSV_FILE_PATH = r"D:\Projects2.0\TueEstate\truestate_assignment_dataset.csv"
BATCH_SIZE = 5000  # Process 5000 rows per batch
PROGRESS_INTERVAL = 10000  # Log progress every 10K rows


async def drop_and_recreate_tables(conn: asyncpg.Connection) -> None:
    """Drop existing tables and recreate with new schema."""
    print("Dropping existing tables...")
    await conn.execute("DROP TABLE IF EXISTS transactions CASCADE")

    print("Creating transactions table with new schema...")
    await conn.execute(
        """
        CREATE TABLE transactions (
            id SERIAL PRIMARY KEY,
            transaction_id INTEGER NOT NULL UNIQUE,
            date DATE NOT NULL,
            customer_id VARCHAR(50) NOT NULL,
            customer_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            age INTEGER NOT NULL,
            customer_region VARCHAR(100) NOT NULL,
            customer_type VARCHAR(50) NOT NULL,
            product_id VARCHAR(50) NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            brand VARCHAR(100) NOT NULL,
            product_category VARCHAR(100) NOT NULL,
            tags TEXT,
            quantity INTEGER NOT NULL,
            price_per_unit DECIMAL(10, 2) NOT NULL,
            discount_percentage DECIMAL(5, 2) NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            final_amount DECIMAL(10, 2) NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            order_status VARCHAR(50) NOT NULL,
            delivery_type VARCHAR(50) NOT NULL,
            store_id VARCHAR(20) NOT NULL,
            store_location VARCHAR(255) NOT NULL,
            salesperson_id VARCHAR(20) NOT NULL,
            employee_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    print("Table created successfully")


async def create_indexes(conn: asyncpg.Connection) -> None:
    """Create indexes after data import for better performance."""
    print("\nCreating indexes...")

    indexes = [
        "CREATE INDEX idx_transaction_id ON transactions(transaction_id)",
        "CREATE INDEX idx_date ON transactions(date)",
        "CREATE INDEX idx_customer_id ON transactions(customer_id)",
        "CREATE INDEX idx_customer_type ON transactions(customer_type)",
        "CREATE INDEX idx_product_id ON transactions(product_id)",
        "CREATE INDEX idx_product_name ON transactions(product_name)",
        "CREATE INDEX idx_brand ON transactions(brand)",
        "CREATE INDEX idx_order_status ON transactions(order_status)",
        "CREATE INDEX idx_delivery_type ON transactions(delivery_type)",
        "CREATE INDEX idx_customer_region ON transactions(customer_region)",
        "CREATE INDEX idx_gender ON transactions(gender)",
        "CREATE INDEX idx_product_category ON transactions(product_category)",
        "CREATE INDEX idx_payment_method ON transactions(payment_method)",
    ]

    for i, index_sql in enumerate(indexes, 1):
        await conn.execute(index_sql)
        print(f"  Created index {i}/{len(indexes)}")

    print("All indexes created successfully")


def parse_csv_row(row: Dict[str, str]) -> tuple:
    """Parse a CSV row and convert to database format."""
    # Handle empty tags field
    tags = row.get("Tags", "").strip()
    if not tags or tags == "":
        tags = None

    # Parse date
    date = datetime.strptime(row["Date"], "%Y-%m-%d").date()

    # Convert numeric fields
    transaction_id = int(row["Transaction ID"])
    age = int(row["Age"])
    quantity = int(row["Quantity"])
    price_per_unit = float(row["Price per Unit"])
    discount_percentage = float(row["Discount Percentage"])
    total_amount = float(row["Total Amount"])
    final_amount = float(row["Final Amount"])

    return (
        transaction_id,
        date,
        row["Customer ID"],
        row["Customer Name"],
        row["Phone Number"],
        row["Gender"],
        age,
        row["Customer Region"],
        row["Customer Type"],
        row["Product ID"],
        row["Product Name"],
        row["Brand"],
        row["Product Category"],
        tags,
        quantity,
        price_per_unit,
        discount_percentage,
        total_amount,
        final_amount,
        row["Payment Method"],
        row["Order Status"],
        row["Delivery Type"],
        row["Store ID"],
        row["Store Location"],
        row["Salesperson ID"],
        row["Employee Name"],
    )


async def import_batch(conn: asyncpg.Connection, batch: List[tuple]) -> int:
    """Import a batch of records."""
    await conn.copy_records_to_table(
        "transactions",
        records=batch,
        columns=[
            "transaction_id",
            "date",
            "customer_id",
            "customer_name",
            "phone_number",
            "gender",
            "age",
            "customer_region",
            "customer_type",
            "product_id",
            "product_name",
            "brand",
            "product_category",
            "tags",
            "quantity",
            "price_per_unit",
            "discount_percentage",
            "total_amount",
            "final_amount",
            "payment_method",
            "order_status",
            "delivery_type",
            "store_id",
            "store_location",
            "salesperson_id",
            "employee_name",
        ],
    )
    return len(batch)


async def import_csv_data(conn: asyncpg.Connection) -> None:
    """Import data from CSV file in batches."""
    print(f"\nImporting data from {CSV_FILE_PATH}")
    print(f"Batch size: {BATCH_SIZE}")

    total_imported = 0
    batch = []
    start_time = datetime.now()

    with open(CSV_FILE_PATH, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                parsed_row = parse_csv_row(row)
                batch.append(parsed_row)

                # Import batch when it reaches batch size
                if len(batch) >= BATCH_SIZE:
                    imported = await import_batch(conn, batch)
                    total_imported += imported
                    batch = []

                    # Log progress
                    if total_imported % PROGRESS_INTERVAL == 0:
                        elapsed = (datetime.now() - start_time).total_seconds()
                        rate = total_imported / elapsed if elapsed > 0 else 0
                        print(f"  Imported {total_imported:,} records ({rate:.0f} records/sec)")

            except Exception as e:
                print(f"Error parsing row {total_imported + len(batch) + 1}: {e}")
                print(f"Row data: {row}")
                continue

        # Import remaining records
        if batch:
            imported = await import_batch(conn, batch)
            total_imported += imported

    elapsed = (datetime.now() - start_time).total_seconds()
    print("\nImport complete!")
    print(f"Total records imported: {total_imported:,}")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Average rate: {total_imported / elapsed:.0f} records/sec")


async def verify_import(conn: asyncpg.Connection) -> None:
    """Verify the imported data."""
    print("\nVerifying imported data...")

    # Count total records
    count = await conn.fetchval("SELECT COUNT(*) FROM transactions")
    print(f"Total records in database: {count:,}")

    # Check sample records
    sample = await conn.fetch("SELECT * FROM transactions LIMIT 3")
    print("\nSample records:")
    for i, record in enumerate(sample, 1):
        print(f"\n  Record {i}:")
        print(f"    Transaction ID: {record['transaction_id']}")
        print(f"    Date: {record['date']}")
        print(f"    Customer: {record['customer_name']} ({record['customer_type']})")
        print(f"    Product: {record['product_name']} - {record['brand']}")
        print(f"    Order Status: {record['order_status']}")
        print(f"    Delivery Type: {record['delivery_type']}")

    # Check categorical distributions
    print("\nData distributions:")

    for field in ["customer_type", "order_status", "delivery_type"]:
        result = await conn.fetch(
            f"SELECT {field}, COUNT(*) as count FROM transactions GROUP BY {field} ORDER BY count DESC"
        )
        print(f"\n  {field.replace('_', ' ').title()}:")
        for row in result:
            print(f"    {row[field]}: {row['count']:,}")


async def main():
    """Main migration function."""
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    if not os.path.exists(CSV_FILE_PATH):
        print(f"ERROR: CSV file not found at {CSV_FILE_PATH}")
        return

    print("=" * 80)
    print("DATABASE MIGRATION: Import from CSV")
    print("=" * 80)
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print(f"CSV File: {CSV_FILE_PATH}")
    print("=" * 80)

    # Warning prompt
    response = input("\n⚠️  WARNING: This will DELETE ALL existing data! Type 'YES' to continue: ")
    if response != "YES":
        print("Migration cancelled")
        return

    try:
        # Connect to database
        print("\nConnecting to database...")
        conn = await asyncpg.connect(DATABASE_URL)

        # Drop and recreate tables
        await drop_and_recreate_tables(conn)

        # Import data
        await import_csv_data(conn)

        # Create indexes
        await create_indexes(conn)

        # Verify import
        await verify_import(conn)

        # Close connection
        await conn.close()

        print("\n" + "=" * 80)
        print("✅ Migration completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
