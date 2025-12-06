"""Transaction controller/routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import get_db
from src.schemas.transaction import (
    TransactionResponse,
    TransactionListQuery,
    TransactionListResponse,
)
from src.services.transaction_service import TransactionService
from src.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    q: str | None = Query(None, description="Search query for customer name or phone"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    sort: str | None = Query("date:desc", description="Sort field and direction"),
    customer_region: List[str] | None = Query(None, description="Filter by customer regions"),
    gender: List[str] | None = Query(None, description="Filter by gender"),
    product_category: List[str] | None = Query(None, description="Filter by product category"),
    tags: List[str] | None = Query(None, description="Filter by tags"),
    payment_method: List[str] | None = Query(None, description="Filter by payment method"),
    age_min: int | None = Query(None, ge=0, le=150, description="Minimum age"),
    age_max: int | None = Query(None, ge=0, le=150, description="Maximum age"),
    date_from: str | None = Query(None, description="Start date (ISO format)"),
    date_to: str | None = Query(None, description="End date (ISO format)"),
    db: AsyncSession = Depends(get_db),
) -> TransactionListResponse:
    """
    List transactions with search, filtering, sorting, and pagination.
    
    - **q**: Search by customer name or phone number
    - **page**: Page number (1-indexed)
    - **limit**: Number of items per page (default: 10, max: 100)
    - **sort**: Sort format 'field:direction' (e.g., 'date:desc', 'quantity:asc', 'customer_name:asc')
    - **Filters**: customer_region, gender, product_category, tags, payment_method, age range, date range
    """
    try:
        # Build query parameters
        query_params = TransactionListQuery(
            q=q,
            page=page,
            limit=limit,
            sort=sort,
            customer_region=customer_region,
            gender=gender,
            product_category=product_category,
            tags=tags,
            payment_method=payment_method,
            age_min=age_min,
            age_max=age_max,
            date_from=date_from,
            date_to=date_to,
        )
        
        # Get service
        service = TransactionService(db)
        
        # List transactions
        result = await service.list_transactions(query_params)
        
        return TransactionListResponse(**result)
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error listing transactions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    """Get a single transaction by ID."""
    try:
        service = TransactionService(db)
        transaction = await service.get_transaction_by_id(transaction_id)
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return TransactionResponse.model_validate(transaction)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting transaction {transaction_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
