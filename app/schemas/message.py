from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ad_id: int = Field(gt=0)
    sender_id: int = Field(gt=0)
    recipient_id: int = Field(gt=0)
    text: str = Field(min_length=1, max_length=2000)


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ad_id: int
    sender_id: int
    recipient_id: int
    text: str
    created_at: datetime