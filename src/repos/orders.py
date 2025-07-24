from src.repos.base import BaseRepository
from src.schemas.orders import OrderDTO


class OrdersRepository(BaseRepository):
    schema = OrderDTO
    