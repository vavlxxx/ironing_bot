import time

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.common.states import UserStates
from src.common.texts import (
    MESSAGE_GREETINGS, 
    MESSAGE_RETURN_BACK, 
    MESSAGE_REGISTRATION_OVER, 
    MESSAGE_CHANGE_PHONE,
    BUTTON_CHANGE_PHONE,
    BUTTON_CHANGE_CODE,
    get_code_input_message
)

from src.services.register import RegisterService
from src.keyboards.reply import (
    get_phone_keyboard, 
    get_actions_keyboard, 
    get_code_input_keyboard
)

from src.config import settings
from src.utils.db_manager import DBManager
from src.utils.functions import parse_phone_number
from src.utils.exceptions import InvalidPhoneNumberException, UserNotFoundException
from src.utils.sms import SMSRuClient


router = Router()


@router.message(StateFilter(None), CommandStart())
async def command_start_handler(message: Message, db: DBManager, state: FSMContext):
    try:
        await RegisterService(db).get_user_by(telegram_id=message.from_user.id)
    except UserNotFoundException:
        await message.answer_photo(caption=MESSAGE_GREETINGS, photo="https://raw.githubusercontent.com/vavlxxx/ironing_bot/refs/heads/main/src/images/Flux_Dev_Illustration_of_laundry_ironing_theme_for_a_Telegram__3.jpg", reply_markup=get_phone_keyboard())
        await state.set_state(UserStates.GET_PHONE)
    else:
        await message.answer_photo(caption=MESSAGE_RETURN_BACK, photo="https://raw.githubusercontent.com/vavlxxx/ironing_bot/refs/heads/main/src/images/Flux_Dev_Illustration_of_laundry_ironing_theme_for_a_Telegram__3.jpg", reply_markup=get_actions_keyboard())


@router.message(StateFilter(UserStates.GET_CODE), F.text == BUTTON_CHANGE_PHONE)
async def change_phone_handler(message: Message, db: DBManager, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.GET_PHONE)
    await message.reply(text=MESSAGE_CHANGE_PHONE, reply_markup=get_phone_keyboard())


@router.message(StateFilter(UserStates.GET_PHONE), or_f(F.text, F.contact))
async def phone_input_handler(message: Message, db: DBManager, state: FSMContext):
    try:
        phone = parse_phone_number(message)
    except InvalidPhoneNumberException:
        await message.answer("Некорректный номер телефона!\n👇 Попробуйте ввести телефон ещё раз:")
        return
    
    smsru_client = SMSRuClient()
    result = await smsru_client.send_sms(phone)
    await state.update_data(phone=phone, code=result.get('code'), timeout=result.get('timeout'))

    await message.answer(
        text=get_code_input_message(phone), 
        reply_markup=get_code_input_keyboard()
    )
    await state.set_state(UserStates.GET_CODE)


@router.message(StateFilter(UserStates.GET_CODE), F.text == BUTTON_CHANGE_CODE)
async def change_code_handler(message: Message, db: DBManager, state: FSMContext):
    data = await state.get_data()
    if data.get('timeout') > time.time():
        await message.answer(f"⏰ Новый код можно будет получить через {int(data.get('timeout') - time.time())} сек.")
        return
    
    smsru_client = SMSRuClient()
    result = await smsru_client.send_sms(data.get('phone'))
    await state.update_data(code=result.get('code'), timeout=result.get('timeout'))

    await message.answer(
        text=get_code_input_message(data.get('phone')), 
        reply_markup=get_code_input_keyboard()
    )


@router.message(StateFilter(UserStates.GET_CODE), F.text)
async def sms_input_handler(message: Message, db: DBManager, state: FSMContext):
    data = await state.get_data()
    if message.text != data.get("code"):
        await message.answer("⚠️ Неверный код. Попробуйте ещё раз.")
        return

    phone = data.get("phone")
    telegram_id = str(message.from_user.id)
    
    try:
        await RegisterService(db).get_user_by(phone=phone)
    except UserNotFoundException:
        await RegisterService(db).create_user(phone=phone, telegram_id=telegram_id)
        await message.answer_photo(caption=MESSAGE_REGISTRATION_OVER, photo="https://raw.githubusercontent.com/vavlxxx/ironing_bot/refs/heads/main/src/images/Flux_Dev_Illustration_of_laundry_ironing_theme_for_a_Telegram__2.jpg", reply_markup=get_actions_keyboard())
    else:
        await RegisterService(db).update_user(phone=phone, telegram_id=telegram_id)
        await message.answer_photo(caption=MESSAGE_REGISTRATION_OVER, photo="https://raw.githubusercontent.com/vavlxxx/ironing_bot/refs/heads/main/src/images/Flux_Dev_Illustration_of_laundry_ironing_theme_for_a_Telegram__2.jpg", reply_markup=get_actions_keyboard())
        await state.clear()
