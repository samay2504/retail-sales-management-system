"""Meta endpoints for filters and system info."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import get_db
from src.schemas.transaction import FilterMetaResponse, HealthResponse
from src.services.transaction_service import TransactionService
from src.utils.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/meta/filters", response_model=FilterMetaResponse)
async def get_filter_metadata(
    db: AsyncSession = Depends(get_db),
) -> FilterMetaResponse:
    """
    Get filter metadata including unique values and counts for all filterable fields.

    Returns:
    - Unique values with counts for: regions, genders, categories, tags, payment methods
    - Min/max ranges for: age, dates
    """
    try:
        service = TransactionService(db)
        metadata = await service.get_filter_metadata()
        return FilterMetaResponse(**metadata)

    except Exception as e:
        logger.error(f"Error getting filter metadata: {e}", exc_info=True)
        return FilterMetaResponse(
            customer_regions=[],
            genders=[],
            product_categories=[],
            tags=[],
            payment_methods=[],
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
    )
