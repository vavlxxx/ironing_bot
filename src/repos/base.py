from sqlalchemy import select


class BaseRepository():
    
    schema = None

    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def get_all_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]

    async def get_all(self):
        return await self.get_all_filtered()
    
    async def get_one_or_none(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj)
    