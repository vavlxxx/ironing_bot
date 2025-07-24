import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.db_manager import DBManager
from src.db import async_SM


async def main():
    async with DBManager(session_factory=async_SM) as db:
        all_orders = await db.orders.get_all()
    
    print(f"Всего заказов: {len(all_orders)}")
    print("Список заказов:\n\n" + "\n".join(map(str, all_orders)))
            

if __name__ == "__main__":
    asyncio.run(main())
    print('Done!')
