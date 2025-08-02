from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10,
    pool_reset_on_return='commit',
    echo=False
)
  
async_SM = async_sessionmaker(bind=engine, expire_on_commit=False)
