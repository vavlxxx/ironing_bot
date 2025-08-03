from aiogram import Router, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.types import Message, CallbackQuery

from src.common.callbacks import UserActions, OrderDetails
from src.common.texts import BUTTON_MY_ORDERS, COMMAND_ORDERS, get_order_description, get_orders_list_message
from src.services.register import RegisterService
from src.config import settings
from src.keyboards.inline import get_back_keyboard, get_user_orders_keyboard

from src.utils.db_manager import DBManager
from src.utils.exceptions import UserNotFoundException


router = Router()
router.message.filter(StateFilter(None))
router.callback_query.filter(StateFilter(None))


@router.message(or_f(F.text == BUTTON_MY_ORDERS, Command(COMMAND_ORDERS)))
async def action_my_first_orders_handler(message: Message, db: DBManager):
    await display_orders_list(message.answer, message.from_user.id, db, settings.DB_BASE_OFFSET)


@router.callback_query(UserActions.filter())
async def action_my_orders_list_handler(callback: CallbackQuery, callback_data: UserActions, db: DBManager):
    offset = int(callback_data.offset)
    await display_orders_list(callback.message.edit_text, callback.from_user.id, db, offset)


@router.callback_query(OrderDetails.filter())
async def action_order_details_handler(callback: CallbackQuery, callback_data: OrderDetails, db: DBManager):
    order_id = int(callback_data.order_id)
    offset = int(callback_data.offset)

    try:
        await RegisterService(db).get_user_by(telegram_id=callback.from_user.id)
    except UserNotFoundException:
        await callback.message.edit_text("⚠️ Произошла ошибка при получении Ваших заказов! Пожалуйста попропробуйте повторить операцию позже.")
    else:
        order_by_user = await db.orders.get_one_or_none(id=order_id)
        await callback.message.edit_text(
            get_order_description(order_by_user),
            reply_markup=get_back_keyboard(offset=offset)
        )


async def display_orders_list(method, telegram_id, db: DBManager, offset: int = 0):
    try:
        user = await RegisterService(db).get_user_by(telegram_id=telegram_id)
    except UserNotFoundException:
        await method("⚠️ Произошла ошибка при получении Ваших заказов! Пожалуйста попропробуйте повторить операцию позже.")
    else:
        orders_by_user = await db.orders.get_all_filtered(user_id=user.id, limit=settings.DB_BASE_LIMIT, offset=offset)
        await method(
            get_orders_list_message(user=user, current_orders=len(orders_by_user), offset=offset),
            reply_markup=get_user_orders_keyboard(orders_by_user, offset=offset, total_orders=user.total_orders)
        )
