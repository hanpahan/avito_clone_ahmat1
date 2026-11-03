from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ad_id: int = Field(gt=0)
    buyer_id: int = Field(gt=0)


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ad_id: int
    buyer_id: int
    seller_id: int
    amount: Decimal
    status: str
    created_at: datetime