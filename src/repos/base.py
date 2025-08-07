from sqlalchemy import insert, select, update
from src.db import engine

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
    
    async def add(self, obj, **params):
        add_obj_stmt = (
            insert(self.model).values(**obj.model_dump(), **params).returning(self.model)
        )
        result = await self.session.execute(add_obj_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj)
    
    async def edit(self, obj, exclude_unset=True, exclude_fields=None, **filter_by):
        exclude_fields = exclude_fields or set()
        to_update = obj.model_dump(exclude=exclude_fields, exclude_unset=exclude_unset)
        if not to_update:
            return
        edit_obj_stmt = update(self.model).filter_by(**filter_by).values(**to_update)
        await self.session.execute(edit_obj_stmt)
