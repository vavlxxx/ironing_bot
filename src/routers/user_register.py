from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.common.states import UserStates
from src.common.texts import get_greetings_message

from src.services.register import RegisterService
from src.keyboards.reply import get_phone_keyboard, get_code_keyboard, get_actions_keyboard

from src.utils.db_manager import DBManager
from src.utils.functions import parse_phone_number
from src.utils.exceptions import InvalidPhoneNumberException, UserNotFoundException
from src.utils.sms import send_sms


router = Router()


@router.message(CommandStart(), StateFilter(None))
async def command_start_handler(message: Message, bot: Bot, db: DBManager, state: FSMContext):
    try:
        await RegisterService(db).get_user_by(telegram_id=message.from_user.id)
    except UserNotFoundException:
        bot_name = (await bot.get_me()).first_name
        msg = get_greetings_message(bot_name)
        await message.answer(msg, reply_markup=get_phone_keyboard())
        await state.set_state(UserStates.GET_PHONE)
        return

    await message.answer("Отлично! Вы уже зарегистрированы!", reply_markup=get_actions_keyboard())


@router.message(StateFilter(UserStates.GET_PHONE), or_f(F.text, F.contact))
async def phone_input_handler(message: Message, db: DBManager, state: FSMContext):
    try:
        phone = parse_phone_number(message)
    except InvalidPhoneNumberException:
        await message.answer("⚠️ Некорректный номер! Попробуйте ещё раз...")
        return

    code, expires = await send_sms(phone=phone, text="Никому не сообщайте этот код: 1234")
    await state.update_data(phone=phone, code=code, expires=expires)

    await message.answer(f"На номер {phone} отправлен код. Введите его для подтверждения", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserStates.GET_CODE)


@router.message(StateFilter(UserStates.GET_CODE), F.text)
async def sms_input_handler(message: Message, db: DBManager, state: FSMContext):
    data = await state.get_data()
    if message.text != data.get("code"):
        await message.answer("⚠️ Неверный код! Попробуйте ещё раз...")
        return
    if datetime.now() > data.get("expires"):
        await message.answer("⚠️ Код истек. Нажмите, чтобы получить новый.", reply_markup=get_code_keyboard())
        return

    phone = data.get("phone")
    
    try:
        await RegisterService(db).get_user_by(phone=phone)
    except UserNotFoundException:
        await RegisterService(db).create_user(phone=phone, telegram_id=message.from_user.id)
        await message.answer("Отлично! Вы успешно зарегистрированы на сайте!", reply_markup=get_actions_keyboard())
        return
    
    await RegisterService(db).update_user(phone=phone, telegram_id=message.from_user.id)
    await message.answer("Отлично! Вы успешно авторизованы на сайте!", reply_markup=get_actions_keyboard())
    await state.clear()
