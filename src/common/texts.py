from src.schemas.users import UserDTO
from src.schemas.orders import OrderDTO
from src.config import settings


BUTTON_MY_ORDERS = "📝 Мои заказы"
BUTTON_CHANGE_CODE = "✉️ Отправить новый код"
BUTTON_SEND_PHONE = "📱 Отправить"
BUTTON_CHANGE_PHONE = "📱 Изменить номер"

COMMAND_ORDERS = "orders"

MESSAGE_CHANGE_PHONE = """
Изменение номера!
👇 Хорошо, поделитесь своим новым номером телефона:
"""

MESSAGE_GREETINGS = """
🌟 Добро пожаловать в "Поглажу"!

Профессиональная глажка одежды с доставкой по городу.

🚀 **Быстро:** Готово за 24 часа
💰 **Выгодно:** Накопительные бонусы  
🏆 **Качественно:** Опытные мастера

Давайте начнем!
👇 Для начала предоставьте свой номер телефона:
"""

MESSAGE_REGISTRATION_OVER = f"""
🎉 Регистрация завершена!

🌟 Поздравляем, теперь вы клиент "Поглажу"!

📋 **Что дальше?**

1️⃣ Посмотрите список своих заказов - /{COMMAND_ORDERS}
2️⃣ Дождитесь уведомления о статусах своих заказов
"""

MESSAGE_RETURN_BACK = f"""
С возвращением! 👋

Рады видеть вас снова в "Поглажу"! 
Что будем гладить сегодня? 😊

/{COMMAND_ORDERS} - Получить список своих заказов
"""

def get_orders_list_message(user: UserDTO, current_orders: int, offset: int):
    return f"""
📋 **История ваших заказов**

Здесь вы можете посмотреть все свои заказы, их статусы и детали.

📊 **Статистика:**
• Всего заказов: {user.total_orders}
• Активных: {user.active_orders}
• Выполненных: {user.completed_orders}

💡 **Подсказка:** Нажмите на номер заказа, чтобы увидеть подробности, статус и возможность оплаты.

👇 **Ваши заказы ({offset+current_orders}/{user.total_orders})**
"""

TEXT_AWAITING_PAYMENT = '⏰ Заказ готов к оплате, но ссылка пока ещё не подготовлена. Пожалуйста, ожидайте... '
TEXT_AWAITING_RECEIPT = '⏰ Заказ успешно оплачен! Пожалуйста, ожидайте пока скачивается квитанция... '

def get_order_description(schema: OrderDTO, statuses) -> str:
    return f"""
🔍 **Заказ: {schema.order_number}**

📆 Дата создания: {schema.created_at}
📍 Адрес доставки: {schema.address_name}
⚡ Текущий статус: {statuses.get(schema.status_id, "Неизвестно")}

📦 Детали заказа
- Общий вес: {schema.total_weight_kg} кг
- Тариф: {schema.tariff_name}
- Цена за кг: {schema.tariff_price_per_kg} ₽/кг

💰 Итоговая стоимость: {schema.total_price}₽

{ TEXT_AWAITING_PAYMENT if schema.payment_url is None and schema.status_id == statuses.get('not_paid', 0) else ''}
{ TEXT_AWAITING_RECEIPT if schema.receipt_url is None and schema.status_id == statuses.get('completed', 0) else ''}
"""

def get_code_input_message(phone):
    return f"""
✉️ На номер {phone} был отправлен код. Введите его для подтверждения регистрации.
{'Сейчас активен тестовый режим, код: `1234`' if settings.SMSRU_MODE == 'TEST' else ''}
"""
