# Create Pydantic schemas

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    received = "received"
    paid = "paid"
    in_progress = "in_progress"
    done = "done"


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    job_description: str
    bill_amount: float


class OrderUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    estimated_completion: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    tracking_number: str
    customer_name: str
    customer_phone: str
    job_description: str
    bill_amount: float
    status: StatusEnum
    estimated_completion: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
