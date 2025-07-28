from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.common.texts import BUTTON_MY_ORDERS, BUTTON_SEND_CODE


def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📱 Отправить', request_contact=True)]],
        resize_keyboard=True,
    )

def get_actions_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_MY_ORDERS)]],
        resize_keyboard=True
    )

def get_code_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_SEND_CODE)]],
        resize_keyboard=True
    )