import sys
import logging
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import settings
from src.db import async_SM
from src.routers.start import router as start_router
from src.common.middlewares import DBMiddleware


dp = Dispatcher()
dp.include_router(start_router)
dp.message.middleware(DBMiddleware(async_SM))

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    print('Done!')
