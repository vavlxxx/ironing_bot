from datetime import datetime
from decimal import Decimal
from pydantic import Field
from src.schemas.base import BaseDTO

class UserDTO(BaseDTO):
    id: int
    phone: str | None = Field(max_length=20)
    bonus_points: int | None
    total_orders: int | None
    total_spent: Decimal | None = Field(max_digits=10, decimal_places=2)
    created_at: datetime | None
    last_login: datetime | None
    