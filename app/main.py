import uvicorn
from fastapi import FastAPI
from app.api.v1 import api_router

from app.database import engine
from app.models.base import Base
import app.models  # регистрирует все модели в metadata

app = FastAPI(
    title="Users and Ads API",
    version="1.0.0",
)

# создаёт недостающие таблицы (payments в т.ч.), существующие не трогает
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)