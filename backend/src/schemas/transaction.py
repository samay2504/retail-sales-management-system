"""Pydantic schemas for API request/response validation."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TransactionBase(BaseModel):
    """Base transaction schema."""
    
    customer_name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=1, max_length=20)
    customer_region: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., min_length=1, max_length=20)
    age: int = Field(..., ge=0, le=150)
    date: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    price_per_unit: float = Field(..., ge=0)
    discount_percentage: float = Field(default=0.0, ge=0, le=100)
    total_amount: float = Field(..., ge=0)
    final_amount: float = Field(..., ge=0)
    product_category: str = Field(..., min_length=1, max_length=100)
    tags: Optional[str] = None
    payment_method: str = Field(..., min_length=1, max_length=50)
    store_id: str = Field(..., min_length=1, max_length=50)
    store_location: str = Field(..., min_length=1, max_length=255)
    salesperson_id: str = Field(..., min_length=1, max_length=50)
    employee_name: str = Field(..., min_length=1, max_length=255)


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class TransactionListQuery(BaseModel):
    """Schema for transaction list query parameters."""
    
    # Search
    q: Optional[str] = Field(None, description="Search query for customer name or phone")
    
    # Pagination
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")
    
    # Sorting
    sort: Optional[str] = Field(
        default="date:desc",
        description="Sort format: field:direction (e.g., date:desc, quantity:asc, customer_name:asc)"
    )
    
    # Filters - Multi-select
    customer_region: Optional[List[str]] = Field(default=None, description="Filter by regions")
    gender: Optional[List[str]] = Field(default=None, description="Filter by gender")
    product_category: Optional[List[str]] = Field(default=None, description="Filter by category")
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
    payment_method: Optional[List[str]] = Field(default=None, description="Filter by payment method")
    
    # Filters - Range
    age_min: Optional[int] = Field(default=None, ge=0, le=150, description="Minimum age")
    age_max: Optional[int] = Field(default=None, ge=0, le=150, description="Maximum age")
    date_from: Optional[str] = Field(default=None, description="Start date (ISO format)")
    date_to: Optional[str] = Field(default=None, description="End date (ISO format)")
    
    @field_validator("sort")
    @classmethod
    def validate_sort(cls, v: Optional[str]) -> Optional[str]:
        """Validate sort parameter format."""
        if v is None:
            return v
        
        allowed_fields = {"date", "quantity", "customer_name"}
        allowed_directions = {"asc", "desc"}
        
        parts = v.split(":")
        if len(parts) != 2:
            raise ValueError("Sort format must be 'field:direction'")
        
        field, direction = parts
        if field not in allowed_fields:
            raise ValueError(f"Sort field must be one of {allowed_fields}")
        if direction not in allowed_directions:
            raise ValueError(f"Sort direction must be one of {allowed_directions}")
        
        return v


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class TransactionListResponse(BaseModel):
    """Response schema for transaction list."""
    
    items: List[TransactionResponse]
    meta: PaginationMeta


class FilterOption(BaseModel):
    """Schema for filter option with count."""
    
    value: str
    count: int


class FilterMetaResponse(BaseModel):
    """Response schema for filter metadata."""
    
    customer_regions: List[FilterOption]
    genders: List[FilterOption]
    product_categories: List[FilterOption]
    tags: List[FilterOption]
    payment_methods: List[FilterOption]
    age_range: dict = Field(default={"min": 0, "max": 100})
    date_range: dict = Field(default={"min": None, "max": None})


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    timestamp: str
    version: str = "1.0.0"
