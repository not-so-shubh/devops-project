from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductDetails(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    sku: str = Field(min_length=2, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    name: str = Field(min_length=2, max_length=160)
    category: str = Field(min_length=2, max_length=80)
    selling_price: Decimal = Field(ge=0, le=9999999999, max_digits=12, decimal_places=2)
    reorder_threshold: int = Field(default=10, ge=0, le=1000000, strict=True)
    description: str = Field(default="", max_length=4000)

    @field_validator("sku")
    @classmethod
    def uppercase_sku(cls, value):
        return value.upper()


class ProductCreate(ProductDetails):
    stock_quantity: int = Field(default=0, ge=0, le=1000000, strict=True)


class ProductOut(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def ensure_utc(cls, value):
        return (
            value.replace(tzinfo=timezone.utc)
            if value.tzinfo is None
            else value.astimezone(timezone.utc)
        )


class Adjustment(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    product_id: int = Field(gt=0, strict=True)
    quantity_change: int = Field(ge=-1000000, le=1000000, strict=True)
    reason: str = Field(min_length=3, max_length=240)

    @field_validator("quantity_change")
    @classmethod
    def nonzero(cls, value):
        if value == 0:
            raise ValueError("Quantity change must be non-zero")
        return value


class MovementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int | None
    product_name: str
    sku: str
    quantity_change: int
    quantity_after: int
    reason: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, value):
        return (
            value.replace(tzinfo=timezone.utc)
            if value.tzinfo is None
            else value.astimezone(timezone.utc)
        )
