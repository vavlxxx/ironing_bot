from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.automap import automap_base

from src.config import settings
from src.repos.orders import OrdersRepository
from src.repos.users import UsersRepository
from src.repos.statuses import StatusesRepository


class DBManager:
    
    def __init__(self, session_factory, models_required=True):
        self.Base = None
        self.models = {}
        self.session_factory = session_factory
        if models_required:
            self._initialize_models()
    

    async def __aenter__(self):
        self.session = self.session_factory()
        self.orders = OrdersRepository(self.session, self.get_model(settings.DB_TABLE_ORDERS))
        self.users = UsersRepository(self.session, self.get_model(settings.DB_TABLE_USERS))
        self.statuses = StatusesRepository(self.session, self.get_model(settings.DB_TABLE_STATUSES))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()


    def get_model(self, table_name: str):
        return self.models.get(table_name)


    def _initialize_models(self):
        sync_engine = create_engine(
            settings.database_url
            .replace('+aiomysql', '+pymysql')
        )
        
        metadata = MetaData()
        metadata.reflect(bind=sync_engine)
        self.Base = automap_base(metadata=metadata)
        self.Base.prepare(autoload_with=sync_engine)
        
        for class_name in self.Base.classes.keys():
            self.models[class_name] = getattr(self.Base.classes, class_name)
        
        sync_engine.dispose()
