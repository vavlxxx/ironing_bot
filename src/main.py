import sys
import logging
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import settings
from src.db import async_SM, engine
from src.utils.db_manager import DBManager
from src.common.middlewares import DBMiddleware

from src.routers.user_register import router as register_router
from src.routers.user_actions import router as actions_router


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_router(register_router)
dp.include_router(actions_router)

dp.message.middleware(DBMiddleware(async_SM))
dp.callback_query.middleware(DBMiddleware(async_SM))

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='markdown')
)


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()
            

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('KeyboardInterrupt!')
