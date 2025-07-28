from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    GET_PHONE = State()
    GET_CODE = State()
    