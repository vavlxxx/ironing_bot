from sqlalchemy import select
from src.repos.base import BaseRepository
from schemas.orders import OrderDTO


class OrdersRepository(BaseRepository):
    schema = OrderDTO
    
    async def get_all_filtered(self, *filter, limit=None, offset=None, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]