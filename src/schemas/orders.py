from datetime import datetime
from decimal import Decimal
from pydantic import Field
from src.schemas.base import BaseDTO


class OrderDTO(BaseDTO):
    id: int
    user_id: int
    order_number: str = Field(max_length=20)
    urgency_id: int
    status_id: int
    total_weight_kg: Decimal = Field(max_digits=5, decimal_places=2)
    base_price: Decimal = Field(max_digits=10, decimal_places=2)
    urgency_price: Decimal | None = Field(max_digits=10, decimal_places=2)
    total_price: Decimal = Field(max_digits=10, decimal_places=2)
    tariff_name: str | None = Field(max_length=100)
    tariff_price_per_kg: Decimal | None = Field(max_digits=6, decimal_places=2)
    notes: str | None
    created_at: datetime | None
    updated_at: datetime | None
    amocrm_lead_id: int | None
    payment_url: str | None = Field(max_length=255)
