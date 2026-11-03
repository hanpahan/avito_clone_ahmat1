from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Ad
from app.schemas.ad import AdCreate


_AD_SORT_FIELDS = {
    "id": Ad.id,
    "price": Ad.price,
    "title": Ad.title,
}


def get_by_id(db: Session, ad_id: int) -> Ad | None:
    return db.get(Ad, ad_id)


def list_with_filters(
    db: Session,
    *,
    query: str | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
    status: str | None = None,
    city: str | None = None,
    district: str | None = None,
    price_min: Decimal | None = None,
    price_max: Decimal | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    offset: int = 0,
    limit: int = 20,
) -> tuple[list[Ad], int]:
    conditions = []
    if query:
        like = f"%{query}%"
        conditions.append(or_(Ad.title.ilike(like), Ad.description.ilike(like)))
    if category_id is not None:
        conditions.append(Ad.category_id == category_id)
    if owner_id is not None:
        conditions.append(Ad.owner_id == owner_id)
    if status is not None:
        conditions.append(Ad.status == status)
    if city is not None:
        conditions.append(Ad.city == city)
    if district is not None:
        conditions.append(Ad.district == district)
    if price_min is not None:
        conditions.append(Ad.price >= price_min)
    if price_max is not None:
        conditions.append(Ad.price <= price_max)

    total = db.scalar(select(func.count()).select_from(Ad).where(*conditions)) or 0

    sort_col = _AD_SORT_FIELDS.get(sort_by, Ad.id)
    order = sort_col.desc() if sort_order == "desc" else sort_col.asc()
    items = db.scalars(
        select(Ad).where(*conditions).order_by(order).offset(offset).limit(limit)
    ).all()
    return list(items), total


def create(db: Session, payload: AdCreate) -> Ad:
    ad = Ad(**payload.model_dump())
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


def update(db: Session, ad: Ad, data: dict) -> Ad:
    for field, value in data.items():
        setattr(ad, field, value)
    db.commit()
    db.refresh(ad)
    return ad


def delete(db: Session, ad: Ad) -> None:
    db.delete(ad)
    db.commit()