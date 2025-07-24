from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.common.states import IntroductionStates
from src.keyboards.reply import get_phone_keyboard
from src.utils.db_manager import DBManager
from src.utils.functions import format_orders_list, format_phone_number


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot, state: FSMContext):
    bot_name = (await bot.get_me()).first_name
    await message.answer(f'🖐️ Привет! Меня зовут {bot_name}')
    await message.answer(f'📱 Для начала предоставьте Ваш номер телефона...', reply_markup=get_phone_keyboard())
    await state.set_state(IntroductionStates.GET_PHONE)


@router.message(StateFilter(IntroductionStates.GET_PHONE), or_f(F.text, F.contact))
async def phone_input_handler(message: Message, db: DBManager, state: FSMContext):
    phone = message.text.strip() if message.contact is None else message.contact.phone_number
    phone = format_phone_number(phone)

    if phone is None or not (phone.startswith("7")):
        await message.answer(
            "⚠️ Пожалуйста, введите корректный номер телефона!",
            reply_markup=get_phone_keyboard(),
        )
        return

    phone_ = f"+{phone}"
    user = await db.users.get_one_or_none(phone=phone_)
    
    if user is None:
        await message.answer(
            "❌ Пользователь с таким номером телефона не найден"
        )
        return
    
    orders_by_user = await db.orders.get_all_filtered(user_id=user.id)
    
    formatted_message = format_orders_list(orders_by_user)
    
    await message.answer(
        formatted_message, 
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )

