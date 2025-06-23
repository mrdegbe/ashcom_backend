# API routes

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.get("/orders/{tracking_number}", response_model=schemas.OrderResponse)
def read_order(tracking_number: str, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_tracking(db, tracking_number)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.patch("/orders/{order_id}", response_model=schemas.OrderResponse)
def update_order(
    order_id: int, updates: schemas.OrderUpdate, db: Session = Depends(get_db)
):
    db_order = crud.update_order(db, order_id, updates)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/orders", response_model=list[schemas.OrderResponse])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip, limit)
