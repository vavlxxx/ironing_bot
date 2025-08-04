from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.common.texts import (
    BUTTON_MY_ORDERS, 
    BUTTON_CHANGE_PHONE,
    BUTTON_SEND_PHONE,
    BUTTON_CHANGE_CODE
)


def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_SEND_PHONE, request_contact=True)]],
        resize_keyboard=True,
    )

def get_code_input_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_CHANGE_CODE)],
            [KeyboardButton(text=BUTTON_CHANGE_PHONE)]
        ],
        resize_keyboard=True,
    )

def get_actions_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_MY_ORDERS)]],
        resize_keyboard=True
    )
