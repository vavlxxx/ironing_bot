from src.repos.base import BaseRepository
from schemas.orders import OrderDTO


class OrdersRepository(BaseRepository):
    schema = OrderDTO
    