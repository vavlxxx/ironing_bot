from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📱 Отправить', request_contact=True)]],
        resize_keyboard=True,
    )
