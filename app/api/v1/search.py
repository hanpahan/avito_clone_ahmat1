from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.ad import AdRead
from app.schemas.common import Page
from app.schemas.user import UserRead
from app.services import search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/users", response_model=Page[UserRead])
def search_users(
    query: str | None = Query(default=None, max_length=100),
    age_min: int | None = Query(default=None, ge=0, le=150),
    age_max: int | None = Query(default=None, ge=0, le=150),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return search_service.search_users(
        db, query=query, age_min=age_min, age_max=age_max, page=page, limit=limit
    )


@router.get("/ads", response_model=Page[AdRead])
def search_ads(
    query: str | None = Query(default=None, max_length=200),
    category_id: int | None = Query(default=None, gt=0),
    owner_id: int | None = Query(default=None, gt=0),
    status_: str | None = Query(default=None, alias="status", max_length=20),
    city: str | None = Query(default=None, max_length=100),
    district: str | None = Query(default=None, max_length=100),
    price_min: Decimal | None = Query(default=None, ge=0),
    price_max: Decimal | None = Query(default=None, ge=0),
    sort_by: str = Query(default="id", pattern="^(id|price|title)$"),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return search_service.search_ads(
        db,
        query=query,
        category_id=category_id,
        owner_id=owner_id,
        status=status_,
        city=city,
        district=district,
        price_min=price_min,
        price_max=price_max,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )