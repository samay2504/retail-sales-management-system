"""Verify CSV field names match our schema."""

import csv

CSV_FILE = r"D:\Projects2.0\TueEstate\truestate_assignment_dataset.csv"

# Expected fields in order based on the import script
EXPECTED_FIELDS = [
    "Transaction ID",
    "Date",
    "Customer ID",
    "Customer Name",
    "Phone Number",
    "Gender",
    "Age",
    "Customer Region",
    "Customer Type",
    "Product ID",
    "Product Name",
    "Brand",
    "Product Category",
    "Tags",
    "Quantity",
    "Price per Unit",
    "Discount Percentage",
    "Total Amount",
    "Final Amount",
    "Payment Method",
    "Order Status",
    "Delivery Type",
    "Store ID",
    "Store Location",
    "Salesperson ID",
    "Employee Name",
]

print("Verifying CSV field names...\n")

with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    actual_fields = reader.fieldnames

    print(f"Expected {len(EXPECTED_FIELDS)} fields")
    print(f"Found {len(actual_fields)} fields")
    print()

    # Check for missing fields
    missing = set(EXPECTED_FIELDS) - set(actual_fields)
    if missing:
        print("❌ MISSING FIELDS:")
        for field in missing:
            print(f"   - {field}")

    # Check for extra fields
    extra = set(actual_fields) - set(EXPECTED_FIELDS)
    if extra:
        print("❌ EXTRA FIELDS:")
        for field in extra:
            print(f"   - {field}")

    # Check if all match
    if not missing and not extra:
        print("✅ All field names match!")
        print("\nField mapping:")
        for i, field in enumerate(EXPECTED_FIELDS, 1):
            print(f"  {i:2d}. {field}")

    # Read one sample row
    row = next(reader)
    print("\n" + "=" * 60)
    print("Sample row values:")
    print("=" * 60)
    for field in EXPECTED_FIELDS[:10]:  # Show first 10
        print(f"{field:25s}: {row[field]}")
