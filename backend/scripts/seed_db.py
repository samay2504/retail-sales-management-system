"""Seed database with sample retail sales data."""

import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy import text

from src.models import AsyncSessionLocal, init_db
from src.models.transaction import Transaction


# Extended Sample data for comprehensive testing
FIRST_NAMES = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
    "David",
    "Barbara",
    "Richard",
    "Susan",
    "Joseph",
    "Jessica",
    "Thomas",
    "Sarah",
    "Charles",
    "Karen",
    "Christopher",
    "Nancy",
    "Daniel",
    "Lisa",
    "Matthew",
    "Betty",
    "Anthony",
    "Margaret",
    "Mark",
    "Sandra",
    "Donald",
    "Ashley",
    "Steven",
    "Kimberly",
    "Paul",
    "Emily",
    "Andrew",
    "Donna",
    "Joshua",
    "Michelle",
    "Kenneth",
    "Carol",
    "Kevin",
    "Amanda",
    "Brian",
    "Dorothy",
    "George",
    "Melissa",
    "Timothy",
    "Deborah",
    "Ronald",
    "Stephanie",
    "Edward",
    "Rebecca",
    "Jason",
    "Sharon",
    "Jeffrey",
    "Laura",
    "Ryan",
    "Cynthia",
    "Jacob",
    "Kathleen",
    "Gary",
    "Amy",
    "Nicholas",
    "Shirley",
    "Eric",
    "Angela",
    "Jonathan",
    "Helen",
    "Stephen",
    "Anna",
    "Larry",
    "Brenda",
    "Justin",
    "Pamela",
    "Scott",
    "Nicole",
    "Brandon",
    "Emma",
    "Benjamin",
    "Samantha",
    "Samuel",
    "Katherine",
    "Raymond",
    "Christine",
    "Gregory",
    "Debra",
    "Frank",
    "Rachel",
    "Alexander",
    "Catherine",
    "Patrick",
    "Carolyn",
    "Jack",
    "Janet",
    "Dennis",
    "Ruth",
    "Jerry",
    "Maria",
    "Tyler",
    "Heather",
    "Aaron",
    "Diane",
    "Jose",
    "Virginia",
    "Adam",
    "Julie",
    "Henry",
    "Joyce",
    "Nathan",
    "Victoria",
    "Douglas",
    "Olivia",
    "Zachary",
    "Kelly",
    "Peter",
    "Christina",
    "Kyle",
    "Lauren",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
    "Gomez",
    "Phillips",
    "Evans",
    "Turner",
    "Diaz",
    "Parker",
    "Cruz",
    "Edwards",
    "Collins",
    "Reyes",
    "Stewart",
    "Morris",
    "Morales",
    "Murphy",
    "Cook",
    "Rogers",
    "Gutierrez",
    "Ortiz",
    "Morgan",
    "Cooper",
    "Peterson",
    "Bailey",
    "Reed",
    "Kelly",
    "Howard",
    "Ramos",
    "Kim",
    "Cox",
    "Ward",
    "Richardson",
    "Watson",
    "Brooks",
    "Chavez",
    "Wood",
    "James",
    "Bennett",
    "Gray",
    "Mendoza",
    "Ruiz",
    "Hughes",
    "Price",
    "Alvarez",
    "Castillo",
    "Sanders",
    "Patel",
    "Myers",
    "Long",
    "Ross",
    "Foster",
    "Jimenez",
    "Powell",
    "Jenkins",
    "Perry",
    "Russell",
]

REGIONS = [
    "North",
    "South",
    "East",
    "West",
    "Central",
    "Northeast",
    "Southeast",
    "Northwest",
    "Southwest",
    "Midwest",
]
GENDERS = ["Male", "Female", "Other", "Prefer not to say"]
CATEGORIES = [
    "Electronics",
    "Smartphones",
    "Laptops & Computers",
    "Smart Home Devices",
    "Audio Equipment",
    "Clothing",
    "Men's Fashion",
    "Women's Fashion",
    "Children's Clothing",
    "Accessories",
    "Food & Beverage",
    "Organic Foods",
    "Snacks & Confectionery",
    "Beverages",
    "Gourmet Foods",
    "Home & Garden",
    "Furniture",
    "Kitchen Appliances",
    "Gardening Tools",
    "Home Decor",
    "Sports & Outdoors",
    "Fitness Equipment",
    "Camping Gear",
    "Sports Apparel",
    "Bicycles",
    "Books & Media",
    "Fiction Books",
    "Non-Fiction Books",
    "Music & Movies",
    "Educational Materials",
    "Toys & Games",
    "Board Games",
    "Video Games",
    "Children's Toys",
    "Puzzles",
    "Health & Beauty",
    "Skincare",
    "Makeup",
    "Personal Care",
    "Supplements",
    "Automotive",
    "Car Parts",
    "Tools",
    "Car Accessories",
    "Maintenance Products",
    "Office Supplies",
    "Stationery",
    "Office Furniture",
    "Technology Accessories",
    "Business Equipment",
]

TAGS_POOL = [
    "bestseller",
    "clearance",
    "seasonal",
    "premium",
    "eco-friendly",
    "new-arrival",
    "limited-edition",
    "sale",
    "popular",
    "trending",
    "discounted",
    "hot-deal",
    "featured",
    "recommended",
    "exclusive",
    "bundle",
    "gift-idea",
    "holiday-special",
    "flash-sale",
    "pre-order",
    "handmade",
    "organic",
    "sustainable",
    "luxury",
    "budget-friendly",
    "top-rated",
    "customer-favorite",
    "award-winning",
    "imported",
    "local",
]

PAYMENT_METHODS = [
    "Credit Card",
    "Visa",
    "MasterCard",
    "American Express",
    "Debit Card",
    "Cash",
    "Digital Wallet",
    "PayPal",
    "Apple Pay",
    "Google Pay",
    "Bank Transfer",
    "Wire Transfer",
    "Cryptocurrency",
    "Gift Card",
    "Store Credit",
    "Buy Now Pay Later",
]

CITIES = [
    "New York, NY",
    "Los Angeles, CA",
    "Chicago, IL",
    "Houston, TX",
    "Phoenix, AZ",
    "Philadelphia, PA",
    "San Antonio, TX",
    "San Diego, CA",
    "Dallas, TX",
    "San Jose, CA",
    "Austin, TX",
    "Jacksonville, FL",
    "Fort Worth, TX",
    "Columbus, OH",
    "Charlotte, NC",
    "San Francisco, CA",
    "Indianapolis, IN",
    "Seattle, WA",
    "Denver, CO",
    "Washington, DC",
    "Boston, MA",
    "El Paso, TX",
    "Nashville, TN",
    "Detroit, MI",
    "Oklahoma City, OK",
    "Portland, OR",
    "Las Vegas, NV",
    "Memphis, TN",
    "Louisville, KY",
    "Baltimore, MD",
    "Milwaukee, WI",
    "Albuquerque, NM",
    "Tucson, AZ",
    "Fresno, CA",
    "Sacramento, CA",
    "Kansas City, MO",
    "Mesa, AZ",
    "Atlanta, GA",
    "Omaha, NE",
    "Colorado Springs, CO",
    "Raleigh, NC",
    "Miami, FL",
    "Long Beach, CA",
    "Virginia Beach, VA",
    "Oakland, CA",
    "Minneapolis, MN",
    "Tulsa, OK",
    "Tampa, FL",
    "Arlington, TX",
    "New Orleans, LA",
]

EMPLOYEE_FIRST = [
    "Alice",
    "Bob",
    "Carol",
    "Dan",
    "Eve",
    "Frank",
    "Grace",
    "Henry",
    "Iris",
    "Jack",
    "Kate",
    "Leo",
    "Mia",
    "Noah",
    "Olivia",
    "Peter",
    "Quinn",
    "Ruby",
    "Sam",
    "Tina",
    "Uma",
    "Victor",
    "Wendy",
    "Xavier",
    "Yara",
    "Zoe",
    "Adam",
    "Bella",
    "Chris",
    "Diana",
    "Ethan",
    "Fiona",
    "George",
    "Hannah",
    "Isaac",
    "Julia",
    "Kevin",
    "Lucy",
    "Mason",
    "Nina",
]

EMPLOYEE_LAST = [
    "Anderson",
    "Baker",
    "Carter",
    "Davis",
    "Evans",
    "Foster",
    "Gray",
    "Hughes",
    "Jackson",
    "King",
    "Lee",
    "Martin",
    "Nelson",
    "Owen",
    "Parker",
    "Quinn",
    "Roberts",
    "Stone",
    "Taylor",
    "White",
    "Young",
    "Adams",
    "Brooks",
    "Clark",
]


def generate_phone_number() -> str:
    """Generate a realistic random phone number with various formats."""
    formats = [
        f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
        f"{random.randint(200, 999)}.{random.randint(100, 999)}.{random.randint(1000, 9999)}",
        f"+1 {random.randint(200, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
    ]
    return random.choice(formats)


def generate_customer_name() -> str:
    """Generate a random customer name."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    # Sometimes add middle initial
    if random.random() < 0.3:
        middle = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"{first} {middle}. {last}"
    return f"{first} {last}"


def generate_employee_name() -> str:
    """Generate a random employee name."""
    first = random.choice(EMPLOYEE_FIRST)
    last = random.choice(EMPLOYEE_LAST)
    return f"{first} {last}"


def generate_transaction() -> dict:
    """Generate a random transaction with realistic variations."""
    customer_name = generate_customer_name()
    phone = generate_phone_number()
    region = random.choice(REGIONS)
    gender = random.choice(GENDERS)

    # Age distribution with realistic bell curve
    age = int(random.gauss(42, 15))  # Mean 42, std dev 15
    age = max(18, min(85, age))  # Clamp between 18 and 85

    # Generate date with non-uniform distribution (more recent transactions)
    days_ago = int(abs(random.gauss(180, 200)))  # Weighted towards recent
    days_ago = min(days_ago, 730)  # Cap at 2 years
    date = (datetime.now() - timedelta(days=days_ago)).isoformat()

    # Quantity with realistic distribution (mostly 1-3, rarely more)
    quantity = random.choices(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[40, 25, 15, 8, 5, 3, 2, 1, 0.5, 0.5]
    )[0]

    # Price with realistic ranges based on category
    category = random.choice(CATEGORIES)

    if "Electronics" in category or "Laptop" in category or "Smart" in category:
        price_per_unit = round(random.uniform(100.0, 2500.0), 2)
    elif "Furniture" in category or "Appliance" in category:
        price_per_unit = round(random.uniform(200.0, 1500.0), 2)
    elif "Automotive" in category:
        price_per_unit = round(random.uniform(50.0, 800.0), 2)
    elif "Clothing" in category or "Fashion" in category:
        price_per_unit = round(random.uniform(15.0, 300.0), 2)
    elif "Food" in category or "Beverage" in category:
        price_per_unit = round(random.uniform(5.0, 100.0), 2)
    else:
        price_per_unit = round(random.uniform(10.0, 500.0), 2)

    # Discount with realistic distribution (most have no discount)
    discount_percentage = random.choices(
        [0, 5, 10, 15, 20, 25, 30, 40, 50], weights=[50, 20, 15, 8, 4, 2, 0.5, 0.3, 0.2]
    )[0]

    total_amount = round(quantity * price_per_unit, 2)
    final_amount = round(total_amount * (1 - discount_percentage / 100), 2)

    # Tags based on discount and randomness
    available_tags = TAGS_POOL.copy()
    if discount_percentage > 0:
        if discount_percentage >= 30:
            available_tags.extend(["clearance", "flash-sale", "hot-deal"])
        elif discount_percentage >= 15:
            available_tags.extend(["sale", "discounted"])

    if final_amount > 500:
        available_tags.extend(["premium", "luxury", "high-end"])

    num_tags = random.randint(0, 4)  # Some transactions have no tags
    tags = (
        ", ".join(random.sample(available_tags, min(num_tags, len(available_tags))))
        if num_tags > 0
        else ""
    )

    payment_method = random.choice(PAYMENT_METHODS)

    # Store IDs with realistic patterns
    store_id = f"STORE-{random.randint(1001, 9999)}"
    store_location = random.choice(CITIES)

    # Employee IDs with realistic patterns
    salesperson_id = f"EMP-{random.randint(100, 999)}"
    employee_name = generate_employee_name()

    return {
        "customer_name": customer_name,
        "phone_number": phone,
        "customer_region": region,
        "gender": gender,
        "age": age,
        "date": date,
        "quantity": quantity,
        "price_per_unit": price_per_unit,
        "discount_percentage": discount_percentage,
        "total_amount": total_amount,
        "final_amount": final_amount,
        "product_category": category,
        "tags": tags,
        "payment_method": payment_method,
        "store_id": store_id,
        "store_location": store_location,
        "salesperson_id": salesperson_id,
        "employee_name": employee_name,
    }


async def seed_database(num_records: int = 1000) -> None:
    """Seed the database with sample transactions."""
    print(f"🌱 Seeding database with {num_records} transactions...")
    print("📊 This will create a comprehensive dataset for testing edge cases.")

    # Initialize database
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(text("SELECT COUNT(*) FROM transactions"))
        count = result.scalar()

        if count > 0:
            print(f"⚠️  Database already contains {count} transactions.")
            response = input("Do you want to clear and reseed? (y/N): ")
            if response.lower() != "y":
                print("❌ Aborted.")
                return

            print("🗑️  Clearing existing data...")
            await session.execute(text("DELETE FROM transactions"))
            # Check if FTS table exists before deleting
            result = await session.execute(
                text(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='transactions_fts'"
                )
            )
            if result.scalar():
                await session.execute(text("DELETE FROM transactions_fts"))
            await session.commit()
            print("✅ Cleared existing data.")

        # Generate and insert transactions in batches
        print(f"⚙️  Generating {num_records} realistic transactions...")
        batch_size = 100
        total_batches = (num_records + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, num_records)
            batch_count = end_idx - start_idx

            transactions = []
            for _ in range(batch_count):
                data = generate_transaction()
                transaction = Transaction(**data)
                transactions.append(transaction)

            session.add_all(transactions)
            await session.commit()

            progress = end_idx
            percentage = (progress / num_records) * 100
            print(
                f"  📝 Progress: {progress}/{num_records} ({percentage:.1f}%) - Batch {batch_num + 1}/{total_batches} completed"
            )

        print(f"✅ Inserted {num_records} transactions successfully!")

        # Create and populate FTS table
        print("🔍 Creating FTS5 virtual table for full-text search...")

        # Check if FTS table exists
        result = await session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions_fts'")
        )
        exists = result.scalar()

        if exists:
            await session.execute(text("DROP TABLE transactions_fts"))
            print("  🗑️  Dropped existing FTS table")

        # Create FTS5 table
        await session.execute(
            text(
                """
            CREATE VIRTUAL TABLE transactions_fts USING fts5(
                customer_name,
                phone_number,
                content='transactions',
                content_rowid='id'
            )
        """
            )
        )
        print("  ✅ Created FTS5 virtual table")

        # Populate FTS table
        await session.execute(
            text(
                """
            INSERT INTO transactions_fts(rowid, customer_name, phone_number)
            SELECT id, customer_name, phone_number FROM transactions
        """
            )
        )

        await session.commit()
        print("  ✅ Populated FTS5 table with search data")

        # Create indexes for performance
        print("📊 Creating database indexes for optimal query performance...")
        indexes = [
            ("idx_customer_name", "customer_name"),
            ("idx_phone_number", "phone_number"),
            ("idx_date", "date"),
            ("idx_quantity", "quantity"),
            ("idx_customer_region", "customer_region"),
            ("idx_gender", "gender"),
            ("idx_age", "age"),
            ("idx_product_category", "product_category"),
            ("idx_payment_method", "payment_method"),
            ("idx_final_amount", "final_amount"),
            ("idx_date_quantity", "date, quantity"),
            ("idx_region_category", "customer_region, product_category"),
            ("idx_payment_date", "payment_method, date"),
        ]

        for idx_name, columns in indexes:
            await session.execute(
                text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON transactions({columns})")
            )
            print(f"  ✅ Created index: {idx_name}")

        await session.commit()
        print("✅ All indexes created successfully!")

        # Generate statistics
        print("\n📈 Database Statistics:")

        # Count by region
        result = await session.execute(
            text(
                "SELECT customer_region, COUNT(*) as count FROM transactions GROUP BY customer_region ORDER BY count DESC"
            )
        )
        regions = result.fetchall()
        print(f"  • Regions: {len(regions)} unique regions")

        # Count by category
        result = await session.execute(
            text(
                "SELECT product_category, COUNT(*) as count FROM transactions GROUP BY product_category ORDER BY count DESC LIMIT 5"
            )
        )
        categories = result.fetchall()
        print("  • Top Categories:")
        for cat, count in categories:
            print(f"    - {cat}: {count} transactions")

        # Date range
        result = await session.execute(text("SELECT MIN(date), MAX(date) FROM transactions"))
        min_date, max_date = result.fetchone()
        print(f"  • Date Range: {min_date[:10]} to {max_date[:10]}")

        # Total revenue
        result = await session.execute(text("SELECT SUM(final_amount) FROM transactions"))
        total_revenue = result.scalar()
        print(f"  • Total Revenue: ${total_revenue:,.2f}")

        # Average transaction
        result = await session.execute(text("SELECT AVG(final_amount) FROM transactions"))
        avg_transaction = result.scalar()
        print(f"  • Average Transaction: ${avg_transaction:,.2f}")

    print("\n🎉 Database seeding completed successfully!")
    print(f"✨ The system is now ready with {num_records} transactions for comprehensive testing!")
    print("💡 You can now test:")
    print("   - Full-text search on customer names and phone numbers")
    print("   - Advanced filtering by region, category, payment method, age, date")
    print("   - Sorting by date, quantity, customer name")
    print("   - Pagination with various page sizes")
    print("   - Edge cases: empty tags, various phone formats, price ranges")


if __name__ == "__main__":
    import sys

    num_records = 1000  # Default to 1000 for comprehensive dataset
    if len(sys.argv) > 1:
        try:
            num_records = int(sys.argv[1])
            if num_records < 10:
                print("⚠️  Minimum 10 records required. Using 10.")
                num_records = 10
            elif num_records > 100000:
                print("⚠️  Maximum 100,000 records recommended. Using 100,000.")
                num_records = 100000
        except ValueError:
            print(f"⚠️  Invalid number '{sys.argv[1]}'. Using default: 1000")
            num_records = 1000

    print("=" * 70)
    print("🏢 TruEstate Retail Sales Management System - Database Seeder")
    print("=" * 70)
    print(f"Target Records: {num_records:,}")
    print("=" * 70)

    asyncio.run(seed_database(num_records))
