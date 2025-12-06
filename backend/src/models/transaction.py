"""Transaction model for retail sales data."""

from sqlalchemy import Column, Integer, String, Float, Text, Date, Index
from src.models.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    """Transaction model representing a retail sale."""

    __tablename__ = "transactions"

    # Primary key (auto-increment for database ID)
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Transaction ID from CSV
    transaction_id = Column(Integer, nullable=False, unique=True, index=True)

    # Customer information
    customer_id = Column(String(50), nullable=False, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    gender = Column(String(20), nullable=False, index=True)
    age = Column(Integer, nullable=False, index=True)
    customer_region = Column(String(100), nullable=False, index=True)
    customer_type = Column(String(50), nullable=False, index=True)  # New, Returning, Loyal

    # Transaction details
    date = Column(Date, nullable=False, index=True)  # Date type
    quantity = Column(Integer, nullable=False, index=True)
    price_per_unit = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)

    # Product information
    product_id = Column(String(50), nullable=False, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=False, index=True)
    product_category = Column(String(100), nullable=False, index=True)
    tags = Column(Text, nullable=True)  # Comma-separated tags

    # Payment and Order
    payment_method = Column(String(50), nullable=False, index=True)
    order_status = Column(
        String(50), nullable=False, index=True
    )  # Completed, Pending, Cancelled, Returned
    delivery_type = Column(
        String(50), nullable=False, index=True
    )  # Standard, Express, Store Pickup

    # Store information
    store_id = Column(String(50), nullable=False, index=True)
    store_location = Column(String(255), nullable=False, index=True)

    # Employee information
    salesperson_id = Column(String(50), nullable=False, index=True)
    employee_name = Column(String(255), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, customer={self.customer_name}, date={self.date})>"

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "phone_number": self.phone_number,
            "gender": self.gender,
            "age": self.age,
            "customer_region": self.customer_region,
            "customer_type": self.customer_type,
            "date": self.date.isoformat() if self.date else None,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "discount_percentage": self.discount_percentage,
            "total_amount": self.total_amount,
            "final_amount": self.final_amount,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "brand": self.brand,
            "product_category": self.product_category,
            "tags": self.tags,
            "payment_method": self.payment_method,
            "order_status": self.order_status,
            "delivery_type": self.delivery_type,
            "store_id": self.store_id,
            "store_location": self.store_location,
            "salesperson_id": self.salesperson_id,
            "employee_name": self.employee_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Composite indexes for common query patterns
Index("idx_transaction_date_quantity", Transaction.date, Transaction.quantity)
Index("idx_transaction_region_category", Transaction.customer_region, Transaction.product_category)
Index("idx_transaction_payment_date", Transaction.payment_method, Transaction.date)
