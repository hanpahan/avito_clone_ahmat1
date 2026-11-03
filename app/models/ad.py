from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(Unicode(200), nullable=False)
    description: Mapped[str] = mapped_column(Unicode(1000), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    city: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    district: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    street: Mapped[str | None] = mapped_column(Unicode(200), nullable=True)
    house: Mapped[str | None] = mapped_column(Unicode(30), nullable=True)