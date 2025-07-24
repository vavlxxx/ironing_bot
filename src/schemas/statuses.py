from pydantic import Field
from src.schemas.base import BaseDTO


class StatusDTO(BaseDTO):
    id: int
    name: str = Field(max_length=50)
    slug: str = Field(max_length=20, alias='code')
    color: str | None = Field(max_length=7)
    description: str | None
    is_active: bool | None
    