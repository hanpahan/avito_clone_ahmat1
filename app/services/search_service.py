from decimal import Decimal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Ad, User
from app.schemas.common import Page


def paginate(db: Session, stmt: Select, page: int, limit: int) -> Page:
    offset = (page - 1) * limit
    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = db.scalar(count_stmt) or 0
    pages = (total + limit - 1) // limit if limit else 0
    items = db.scalars(stmt.offset(offset).limit(limit)).all()
    return Page(items=items, page=page, limit=limit, total=total, pages=pages)


def search_users(
    db: Session,
    *,
    query: str | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    page: int = 1,
    limit: int = 20,
) -> Page[User]:
    stmt = select(User)
    if query:
        like = f"%{query}%"
        stmt = stmt.where(or_(User.name.ilike(like), User.email.ilike(like)))
    if age_min is not None:
        stmt = stmt.where(User.age >= age_min)
    if age_max is not None:
        stmt = stmt.where(User.age <= age_max)
    return paginate(db, stmt.order_by(User.id), page, limit)


_AD_SORT_FIELDS = {
    "id": Ad.id,
    "price": Ad.price,
    "title": Ad.title,
}


def search_ads(
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
    page: int = 1,
    limit: int = 20,
) -> Page[Ad]:
    stmt = select(Ad)
    if query:
        like = f"%{query}%"
        stmt = stmt.where(or_(Ad.title.ilike(like), Ad.description.ilike(like)))
    if category_id is not None:
        stmt = stmt.where(Ad.category_id == category_id)
    if owner_id is not None:
        stmt = stmt.where(Ad.owner_id == owner_id)
    if status is not None:
        stmt = stmt.where(Ad.status == status)
    if city is not None:
        stmt = stmt.where(Ad.city == city)
    if district is not None:
        stmt = stmt.where(Ad.district == district)
    if price_min is not None:
        stmt = stmt.where(Ad.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(Ad.price <= price_max)

    sort_col = _AD_SORT_FIELDS.get(sort_by, Ad.id)
    stmt = stmt.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc())
    return paginate(db, stmt, page, limit)