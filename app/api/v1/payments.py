from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.common import Page
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    try:
        return payment_service.create_payment(db, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=Page[PaymentRead])
def list_payments(
    user_id: int = Query(gt=0),
    role: str = Query(default="buyer", pattern="^(buyer|seller)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return payment_service.list_payments(db, user_id, role=role, page=page, limit=limit)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return payment_service.get_payment(db, payment_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{payment_id}/confirm", response_model=PaymentRead)
def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return payment_service.confirm_payment(db, payment_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/{payment_id}/refund", response_model=PaymentRead)
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return payment_service.refund_payment(db, payment_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc