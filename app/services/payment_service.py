from sqlalchemy.orm import Session

from app.repositories import ad_repo, payment_repo
from app.schemas.common import Page
from app.schemas.payment import PaymentCreate, PaymentRead


def create_payment(db: Session, payload: PaymentCreate) -> PaymentRead:
    ad = ad_repo.get_by_id(db, payload.ad_id)
    if ad is None:
        raise LookupError("Ad not found")
    if ad.owner_id == payload.buyer_id:
        raise ValueError("Cannot buy your own ad")
    if ad.status != "active":
        raise ValueError("Ad is not available for purchase")
    if payment_repo.get_active_for_ad(db, ad.id) is not None:
        raise ValueError("Ad already has an active payment")
    return PaymentRead.model_validate(payment_repo.create(db, ad, payload))


def get_payment(db: Session, payment_id: int) -> PaymentRead:
    payment = payment_repo.get_by_id(db, payment_id)
    if payment is None:
        raise LookupError("Payment not found")
    return PaymentRead.model_validate(payment)


def list_payments(
    db: Session, user_id: int, *, role: str = "buyer", page: int = 1, limit: int = 20
) -> Page[PaymentRead]:
    offset = (page - 1) * limit
    if role == "seller":
        items, total = payment_repo.list_for_seller(db, user_id, offset=offset, limit=limit)
    else:
        items, total = payment_repo.list_for_buyer(db, user_id, offset=offset, limit=limit)
    return Page[PaymentRead](
        items=[PaymentRead.model_validate(p) for p in items], total=total
    )


def confirm_payment(db: Session, payment_id: int) -> PaymentRead:
    payment = payment_repo.get_by_id(db, payment_id)
    if payment is None:
        raise LookupError("Payment not found")
    if payment.status != "pending":
        raise ValueError("Payment is not pending")
    return PaymentRead.model_validate(payment_repo.update_status(db, payment, "completed"))


def refund_payment(db: Session, payment_id: int) -> PaymentRead:
    payment = payment_repo.get_by_id(db, payment_id)
    if payment is None:
        raise LookupError("Payment not found")
    if payment.status != "completed":
        raise ValueError("Only completed payments can be refunded")
    return PaymentRead.model_validate(payment_repo.update_status(db, payment, "refunded"))