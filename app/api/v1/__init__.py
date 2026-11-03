from fastapi import APIRouter

from . import ads, payments, search, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(ads.router)
api_router.include_router(search.router)
api_router.include_router(payments.router)

__all__ = ["api_router"]