"""Script to verify no Pydantic deprecation warnings."""
import sys
import warnings

# Capture warnings
warnings.simplefilter("always", DeprecationWarning)

# Track if any Pydantic warnings are found
pydantic_warnings = []


def warning_handler(message, category, filename, lineno, file=None, line=None):
    """Custom warning handler to capture Pydantic warnings."""
    if "pydantic" in str(message).lower() or "pydantic" in filename.lower():
        pydantic_warnings.append({
            "message": str(message),
            "category": category.__name__,
            "filename": filename,
            "lineno": lineno,
        })


# Set custom warning handler
warnings.showwarning = warning_handler

# Import all modules that use Pydantic
try:
    print("Importing Pydantic models and schemas...")
    
    from src.config import settings
    from src.models.transaction import Transaction
    from src.schemas.transaction import (
        TransactionCreate,
        TransactionResponse,
        TransactionListQuery,
    )
    
    print("✓ All imports successful")
    
    # Test instantiation
    print("\nTesting model instantiation...")
    
    query = TransactionListQuery(
        q="test",
        page=1,
        limit=10,
        sort="date:desc",
    )
    print("✓ TransactionListQuery instantiated")
    
    # Check for warnings
    if pydantic_warnings:
        print("\n❌ FAILED: Pydantic deprecation warnings found:")
        for warning in pydantic_warnings:
            print(f"\n  File: {warning['filename']}:{warning['lineno']}")
            print(f"  Category: {warning['category']}")
            print(f"  Message: {warning['message']}")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: No Pydantic deprecation warnings found!")
        sys.exit(0)

except Exception as e:
    print(f"\n❌ ERROR: Failed to import or instantiate models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
