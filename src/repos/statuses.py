from src.repos.base import BaseRepository
from schemas.statuses import StatusDTO


class StatusesRepository(BaseRepository):
    schema = StatusDTO
    