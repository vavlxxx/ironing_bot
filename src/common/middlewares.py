from aiogram import BaseMiddleware

from src.utils.db_manager import DBManager


class DBMiddleware(BaseMiddleware):

    def __init__(self, session_factory):
        self.db_manager = DBManager(session_factory)

    async def __call__(self, handler, event, data):
        async with self.db_manager as db:
            data['db'] = db
            return await handler(event, data)
        