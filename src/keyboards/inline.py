from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from src.config import settings
from src.common.callbacks import UserActions, OrderDetails


def get_user_orders_keyboard(orders_by_user: list, offset: int, total_orders: int):
    keyboard = InlineKeyboardBuilder()
    for order in orders_by_user:
        keyboard.row(
            InlineKeyboardButton(
                text=f"📋 Заказ #{order.order_number}",
                callback_data=OrderDetails(offset=f"{offset}", order_id=f"{order.id}").pack()
            )
        )

    navigation_buttons = []
    if offset > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="<<<", 
                callback_data=UserActions(offset=f"{offset - settings.DB_BASE_LIMIT}").pack()
            ) 
        )
    if offset + len(orders_by_user) < total_orders:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=">>>", 
                callback_data=UserActions(offset=f"{offset + settings.DB_BASE_LIMIT}").pack()
            ) 
        )

    if navigation_buttons:
        keyboard.row(*navigation_buttons)
    return keyboard.as_markup()


def get_back_keyboard(offset: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
                InlineKeyboardButton(
                    text="◀️ Вернуться назад", 
                    callback_data=UserActions(offset=f"{offset}").pack()
                )
            ]]
        )
