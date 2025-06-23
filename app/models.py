# Define the `orders` model

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base
import enum


class StatusEnum(str, enum.Enum):
    received = "received"
    paid = "paid"
    in_progress = "in_progress"
    done = "done"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    job_description = Column(Text)
    bill_amount = Column(Numeric(10, 2))
    status = Column(Enum(StatusEnum), default=StatusEnum.received)
    estimated_completion = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
