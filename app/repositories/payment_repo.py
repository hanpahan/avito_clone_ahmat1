from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Ad, Payment
from app.schemas.payment import PaymentCreate


ACTIVE_STATUSES = ("pending", "completed")


def get_by_id(db: Session, payment_id: int) -> Payment | None:
    return db.get(Payment, payment_id)


def get_active_for_ad(db: Session, ad_id: int) -> Payment | None:
    return db.scalar(
        select(Payment).where(
            Payment.ad_id == ad_id, Payment.status.in_(ACTIVE_STATUSES)
        )
    )


def list_for_buyer(
    db: Session, buyer_id: int, *, offset: int = 0, limit: int = 20
) -> tuple[list[Payment], int]:
    return _list(db, Payment.buyer_id == buyer_id, offset, limit)


def list_for_seller(
    db: Session, seller_id: int, *, offset: int = 0, limit: int = 20
) -> tuple[list[Payment], int]:
    return _list(db, Payment.seller_id == seller_id, offset, limit)


def _list(db: Session, cond, offset: int, limit: int) -> tuple[list[Payment], int]:
    total = db.scalar(select(func.count()).select_from(Payment).where(cond)) or 0
    items = db.scalars(
        select(Payment).where(cond).order_by(Payment.id.desc()).offset(offset).limit(limit)
    ).all()
    return list(items), total


def create(db: Session, ad: Ad, payload: PaymentCreate) -> Payment:
    payment = Payment(
        ad_id=ad.id,
        buyer_id=payload.buyer_id,
        seller_id=ad.owner_id,
        amount=ad.price,
        status="pending",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def update_status(db: Session, payment: Payment, status: str) -> Payment:
    payment.status = status
    db.commit()
    db.refresh(payment)
    return payment