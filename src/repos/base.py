from sqlalchemy import select


class BaseRepository():

    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def get_all_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all(self):
        return await self.get_all_filtered()
    