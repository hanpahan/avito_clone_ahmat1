from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.ad import AdCreate, AdRead, AdUpdate
from app.schemas.common import Page
from app.services import ad_service, search_service

router = APIRouter(prefix="/ads", tags=["ads"])


@router.get("", response_model=Page[AdRead])
def list_ads(
    owner_id: int | None = Query(default=None, gt=0),
    category_id: int | None = Query(default=None, gt=0),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return search_service.search_ads(
        db,
        owner_id=owner_id,
        category_id=category_id,
        page=page,
        limit=limit,
    )


@router.get("/{ad_id}", response_model=AdRead)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    try:
        return ad_service.get_ad(db, ad_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=AdRead, status_code=status.HTTP_201_CREATED)
def create_ad(payload: AdCreate, db: Session = Depends(get_db)):
    try:
        return ad_service.create_ad(db, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{ad_id}", response_model=AdRead)
def update_ad(ad_id: int, payload: AdUpdate, db: Session = Depends(get_db)):
    try:
        return ad_service.update_ad(db, ad_id, payload)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    try:
        ad_service.delete_ad(db, ad_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc