# Database Migration Guide

## Overview
Migrate from 1,000 test records to 1,000,000 production records from CSV file with expanded schema.

## New Fields Added
1. `transaction_id` - Unique transaction identifier (Integer)
2. `customer_id` - Customer identifier (CUST-#####)
3. `customer_type` - New/Returning/Loyal
4. `product_id` - Product identifier (PROD-####)
5. `product_name` - Product name
6. `brand` - Product brand
7. `order_status` - Completed/Pending/Cancelled/Returned
8. `delivery_type` - Standard/Express/Store Pickup

## Files Modified

### Backend
- ✅ `src/models/transaction.py` - Added 8 new columns with indexes
- ✅ `src/schemas/transaction.py` - Updated TransactionBase and TransactionListQuery
- ✅ `src/services/query_builder.py` - Added new filters and search fields
- ✅ `scripts/import_from_csv.py` - New migration script

### Frontend
- ✅ `src/types/api.ts` - Updated Transaction interface and filter types

## Testing Locally (Optional but Recommended)

1. **Create test database:**
   ```powershell
   # Use local PostgreSQL or create test database on Render
   ```

2. **Create test CSV (1000 records):**
   ```powershell
   cd d:\Projects2.0\TueEstate
   Get-Content truestate_assignment_dataset.csv -TotalCount 1001 | Out-File -FilePath backend\scripts\test_sample.csv -Encoding utf8
   ```

3. **Update import script temporarily:**
   Edit `backend/scripts/import_from_csv.py`:
   - Change `CSV_FILE_PATH` to `test_sample.csv`
   - Change `DATABASE_URL` to test database

4. **Run migration:**
   ```powershell
   cd d:\Projects2.0\TueEstate\backend
   python scripts/import_from_csv.py
   ```

5. **Test API:**
   ```powershell
   cd d:\Projects2.0\TueEstate\backend
   python -m uvicorn src.main:app --reload
   ```
   - Visit: http://localhost:8000/docs
   - Test endpoints: `/api/transactions`, `/api/filters`

## Production Migration

### Prerequisites
⚠️ **IMPORTANT:** This will delete all existing data (1000 test records)

1. **Backup current database (if needed):**
   ```bash
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   ```

2. **Ensure CSV file is accessible:**
   - File: `D:\Projects2.0\TueEstate\truestate_assignment_dataset.csv`
   - Size: 1,000,000 records

### Step 1: Run Migration Script

```powershell
cd d:\Projects2.0\TueEstate\backend

# Ensure environment variables are set
$env:DATABASE_URL = "postgresql://truestate_prod_user:0vjEVitjfpiAxi3VE9ppR5XcFojPRph1@dpg-d4q30nqli9vc739mg5ng-a.virginia-postgres.render.com/truestate_prod"

# Run migration (will prompt for confirmation)
python scripts/import_from_csv.py
```

**Expected output:**
```
Database: dpg-d4q30nqli9vc739mg5ng-a.virginia-postgres.render.com/truestate_prod
CSV File: D:\Projects2.0\TueEstate\truestate_assignment_dataset.csv
⚠️  WARNING: This will DELETE ALL existing data! Type 'YES' to continue: YES

Connecting to database...
Dropping existing tables...
Creating transactions table with new schema...
Table created successfully

Importing data from D:\Projects2.0\TueEstate\truestate_assignment_dataset.csv
Batch size: 5000
  Imported 10,000 records (2000 records/sec)
  Imported 20,000 records (2100 records/sec)
  ...
  Imported 1,000,000 records (2050 records/sec)

Import complete!
Total records imported: 1,000,000
Total time: 487.80 seconds
Average rate: 2050 records/sec

Creating indexes...
  Created index 1/13
  Created index 2/13
  ...
  Created index 13/13
All indexes created successfully

Verifying imported data...
Total records in database: 1,000,000

Sample records:
  Record 1:
    Transaction ID: 1
    Date: 2024-01-01
    Customer: Emily Jones (Returning)
    Product: Face Cream - Neutrogena
    Order Status: Cancelled
    Delivery Type: Standard

Data distributions:
  Customer Type:
    Returning: 333,889
    Loyal: 332,415
    New: 333,696

  Order Status:
    Cancelled: 250,456
    Returned: 249,519
    Completed: 249,834
    Pending: 250,191

  Delivery Type:
    Standard: 333,793
    Express: 333,154
    Store Pickup: 333,053

✅ Migration completed successfully!
```

**Estimated time:** 8-10 minutes

### Step 2: Verify Backend

```powershell
# Test health endpoint
curl https://retail-sales-management-system-96ml.onrender.com/api/health

# Test transactions endpoint
curl "https://retail-sales-management-system-96ml.onrender.com/api/transactions?page=1&limit=10"

# Test filters endpoint
curl https://retail-sales-management-system-96ml.onrender.com/api/filters
```

**Expected response from /api/filters should include:**
```json
{
  "customer_regions": [...],
  "customer_types": [
    {"value": "Returning", "count": 333889},
    {"value": "New", "count": 333696},
    {"value": "Loyal", "count": 332415}
  ],
  "brands": [...],
  "order_statuses": [
    {"value": "Cancelled", "count": 250456},
    {"value": "Returned", "count": 249519},
    {"value": "Completed", "count": 249834},
    {"value": "Pending", "count": 250191}
  ],
  "delivery_types": [
    {"value": "Standard", "count": 333793},
    {"value": "Express", "count": 333154},
    {"value": "Store Pickup", "count": 333053}
  ]
}
```

### Step 3: Deploy Backend to Render

Render will auto-deploy when you push to GitHub:

```powershell
cd d:\Projects2.0\TueEstate
git add .
git commit -m "feat: expand schema with 8 new fields and CSV import for 1M records"
git push origin main
```

Monitor deployment at: https://dashboard.render.com/

### Step 4: Deploy Frontend to GitHub Pages

```powershell
cd d:\Projects2.0\TueEstate\frontend

# Build and deploy
npm run deploy
```

Wait for GitHub Actions to complete: https://github.com/Samay2504/retail-sales-management-system/actions

### Step 5: Verify Production

1. **Test frontend:** https://samay2504.github.io/retail-sales-management-system
   - Check that new fields display correctly
   - Test new filters (Customer Type, Brand, Order Status, Delivery Type)
   - Test search with product names, brands
   - Verify pagination works with 1M records

2. **Test API directly:**
   ```powershell
   # Test with new filters
   curl "https://retail-sales-management-system-96ml.onrender.com/api/transactions?customer_type=Loyal&order_status=Completed&page=1&limit=10"
   
   # Test search with product name
   curl "https://retail-sales-management-system-96ml.onrender.com/api/transactions?q=Neutrogena&page=1&limit=10"
   ```

## Rollback Plan

If migration fails or issues are found:

1. **Restore from backup:**
   ```bash
   psql $DATABASE_URL < backup_YYYYMMDD.sql
   ```

2. **Revert code changes:**
   ```powershell
   git revert HEAD
   git push origin main
   ```

## Performance Notes

- Import rate: ~2000 records/second
- Total import time: 8-10 minutes
- Index creation: 1-2 minutes
- Database size: ~200-300 MB (for 1M records)

## Troubleshooting

### Import fails with connection timeout
- Increase connection timeout in asyncpg.connect()
- Reduce BATCH_SIZE from 5000 to 2000

### Import fails with memory error
- Reduce BATCH_SIZE to 1000
- Import will take longer but use less memory

### Indexes creation slow
- Normal for large datasets
- Can take 2-5 minutes for all indexes

### API slow after migration
- Check if indexes were created: `SELECT * FROM pg_indexes WHERE tablename = 'transactions'`
- Verify query plans: Add EXPLAIN ANALYZE to slow queries

## New API Features Available

### New Filter Parameters
- `customer_type`: Filter by New/Returning/Loyal
- `brand`: Filter by product brand
- `order_status`: Filter by Completed/Pending/Cancelled/Returned
- `delivery_type`: Filter by Standard/Express/Store Pickup

### Enhanced Search
Search now includes:
- Product names
- Brand names
- Customer IDs
- Product IDs

Example:
```
GET /api/transactions?q=Neutrogena&customer_type=Loyal&order_status=Completed
```

## Schema Differences

| Field | Old Schema | New Schema |
|-------|-----------|------------|
| transaction_id | ❌ Not present | ✅ Integer, unique, indexed |
| customer_id | ❌ Not present | ✅ String(50), indexed |
| customer_type | ❌ Not present | ✅ String(50), indexed |
| product_id | ❌ Not present | ✅ String(50), indexed |
| product_name | ❌ Not present | ✅ String(255), indexed |
| brand | ❌ Not present | ✅ String(100), indexed |
| order_status | ❌ Not present | ✅ String(50), indexed |
| delivery_type | ❌ Not present | ✅ String(50), indexed |

All existing fields remain unchanged.
