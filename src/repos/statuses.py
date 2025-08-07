from src.repos.base import BaseRepository
from schemas.statuses import StatusDTO


class StatusesRepository(BaseRepository):
    schema = StatusDTO
    
    async def get_all(self):
        statuses = await self.get_all_filtered()
        result = {}
        for status in statuses:
            result[status.slug] = status.id
            result[status.id] = status.name
        return result