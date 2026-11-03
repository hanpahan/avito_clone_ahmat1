from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    owner_id: int = Field(gt=0)
    category_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=1000)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    status: str = Field(default="active", min_length=1, max_length=20)
    city: str = Field(min_length=1, max_length=100)
    district: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=200)
    house: str = Field(min_length=1, max_length=30)


class AdUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    category_id: int | None = Field(default=None, gt=0)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    status: str | None = Field(default=None, min_length=1, max_length=20)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    district: str | None = Field(default=None, min_length=1, max_length=100)
    street: str | None = Field(default=None, min_length=1, max_length=200)
    house: str | None = Field(default=None, min_length=1, max_length=30)

    @model_validator(mode="after")
    def reject_null_values(self):
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Updated fields cannot be null")
        return self


class AdRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    category_id: int | None
    title: str
    description: str
    price: Decimal
    status: str
    city: str | None
    district: str | None
    street: str | None
    house: str | None