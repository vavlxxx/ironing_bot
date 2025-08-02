from aiogram import Router, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.types import Message

from src.common.texts import BUTTON_MY_ORDERS, COMMAND_ORDERS
from src.services.register import RegisterService
from src.utils.db_manager import DBManager
from src.utils.functions import format_orders_list
from src.utils.exceptions import UserNotFoundException


router = Router()


@router.message(StateFilter(None), or_f(F.text == BUTTON_MY_ORDERS, Command(COMMAND_ORDERS)))
async def action_my_orders_handler(message: Message, db: DBManager):
    try:
        user = await RegisterService(db).get_user_by(telegram_id=message.from_user.id)
    except UserNotFoundException:
        await message.answer("⚠️ Произошла ошибка при получении Ваших заказов! Пожалуйста попропробуйте повторить операцию позже.")

    orders_by_user = await db.orders.get_all_filtered(user_id=user.id)

    await message.answer(
        format_orders_list(orders_by_user),
        parse_mode="Markdown"
    )
