from aiogram.filters.callback_data import CallbackData


class UserActions(CallbackData, prefix="act"):
    offset: str

class OrderDetails(UserActions, prefix="det"):
    order_id: str
