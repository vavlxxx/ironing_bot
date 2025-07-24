from aiogram.fsm.state import StatesGroup, State


class IntroductionStates(StatesGroup):
    GET_PHONE = State()
    