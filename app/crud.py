# CRUD Operations

from sqlalchemy.orm import Session
from . import models, schemas, utils
import uuid


def create_order(db: Session, order: schemas.OrderCreate):
    tracking_number = f"ASHCOM-{uuid.uuid4().hex[:8].upper()}"
    db_order = models.Order(
        tracking_number=tracking_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        job_description=order.job_description,
        bill_amount=order.bill_amount,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 📲 Send confirmation message
    message = (
        f"Hello {db_order.customer_name},\n"
        f"Your ASHCOM order has been received.\n"
        f"Tracking #: {db_order.tracking_number}\n"
        f"Bill: GHS {db_order.bill_amount}\n"
        f"We'll notify you once payment is received. Thank you!"
    )
    utils.send_whatsapp_message(db_order.customer_phone, message)

    return db_order


def get_order_by_tracking(db: Session, tracking_number: str):
    return (
        db.query(models.Order)
        .filter(models.Order.tracking_number == tracking_number)
        .first()
    )


def update_order(db: Session, order_id: int, updates: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)

        # 📲 Send relevant update
        if updates.status == models.StatusEnum.paid:
            message = (
                f"Hello {db_order.customer_name},\n"
                f"We've received your payment for order {db_order.tracking_number}.\n"
                f"Estimated completion: {db_order.estimated_completion}."
            )
            utils.send_whatsapp_message(db_order.customer_phone, message)

        if updates.status == models.StatusEnum.done:
            message = (
                f"Hello {db_order.customer_name},\n"
                f"Your order {db_order.tracking_number} is ready for pickup.\n"
                f"Thank you for choosing ASHCOM!"
            )
            utils.send_whatsapp_message(db_order.customer_phone, message)

    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()
