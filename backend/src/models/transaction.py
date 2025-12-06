"""Transaction model for retail sales data."""

from sqlalchemy import Column, Integer, String, Float, Text, Index
from src.models.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    """Transaction model representing a retail sale."""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Customer information
    customer_name = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    customer_region = Column(String(100), nullable=False, index=True)
    gender = Column(String(20), nullable=False, index=True)
    age = Column(Integer, nullable=False, index=True)

    # Transaction details
    date = Column(String(50), nullable=False, index=True)  # ISO format
    quantity = Column(Integer, nullable=False, index=True)
    price_per_unit = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)

    # Product information
    product_category = Column(String(100), nullable=False, index=True)
    tags = Column(Text, nullable=True)  # Comma-separated tags

    # Payment
    payment_method = Column(String(50), nullable=False, index=True)

    # Store information
    store_id = Column(String(50), nullable=False)
    store_location = Column(String(255), nullable=False)

    # Employee information
    salesperson_id = Column(String(50), nullable=False)
    employee_name = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, customer={self.customer_name}, date={self.date})>"

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "phone_number": self.phone_number,
            "customer_region": self.customer_region,
            "gender": self.gender,
            "age": self.age,
            "date": self.date,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "discount_percentage": self.discount_percentage,
            "total_amount": self.total_amount,
            "final_amount": self.final_amount,
            "product_category": self.product_category,
            "tags": self.tags,
            "payment_method": self.payment_method,
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
