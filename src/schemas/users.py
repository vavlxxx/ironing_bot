from datetime import datetime
from decimal import Decimal
from pydantic import Field
from src.schemas.base import BaseDTO


class UserRequestDTO(BaseDTO):
    phone: str = Field(max_length=20)
    bonus_points: int | None = Field(default=None)
    total_orders: int | None = Field(default=None)
    total_spent: Decimal | None = Field(None, max_digits=10, decimal_places=2)
    telegram_id: str | None = Field(default=None)


class UserDTO(UserRequestDTO):
    id: int
    created_at: datetime | None = Field(default=None)
    last_login: datetime | None = Field(default=None)
