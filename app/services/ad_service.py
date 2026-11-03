from sqlalchemy.orm import Session

from app.models import Ad, Category, User
from app.schemas.ad import AdCreate, AdUpdate


def get_ad(db: Session, ad_id: int) -> Ad:
    ad = db.get(Ad, ad_id)
    if ad is None:
        raise LookupError("Ad not found")
    return ad


def create_ad(db: Session, payload: AdCreate) -> Ad:
    if db.get(User, payload.owner_id) is None:
        raise LookupError("Owner not found")
    if payload.category_id is not None and db.get(Category, payload.category_id) is None:
        raise LookupError("Category not found")

    ad = Ad(**payload.model_dump())
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


def update_ad(db: Session, ad_id: int, payload: AdUpdate) -> Ad:
    ad = get_ad(db, ad_id)
    data = payload.model_dump(exclude_unset=True)
    category_id = data.get("category_id")
    if category_id is not None and db.get(Category, category_id) is None:
        raise LookupError("Category not found")

    for field, value in data.items():
        setattr(ad, field, value)

    db.commit()
    db.refresh(ad)
    return ad


def delete_ad(db: Session, ad_id: int) -> None:
    ad = get_ad(db, ad_id)
    db.delete(ad)
    db.commit()