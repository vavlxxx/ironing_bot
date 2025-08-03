from src.schemas.users import UserDTO
from src.schemas.orders import OrderDTO

BUTTON_MY_ORDERS = "📝 Мои заказы"
BUTTON_SEND_CODE = "📧 Отправить новый код"

COMMAND_ORDERS = "orders"

ORDER_STATUSES = {
    1 : "🛑 Не оплачен",
    2 : "📝 В работе",
    3 : "✅ Заказ готов",
    4 : "❌ Заказ отменен",
    5 : "⏳ Новый",
}

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

Поздравляем, теперь вы клиент "Поглажу"!

📋 **Что дальше:**
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

def get_order_description(schema: OrderDTO) -> str:
    return f"""
🔍 **Заказ: {schema.order_number}**

📆 Дата создания: {schema.created_at}
📍 Адрес доставки: {schema.address_name}
⚡ Текущий статус: {ORDER_STATUSES[schema.status_id]}

📦 Детали заказа
- Общий вес: {schema.total_weight_kg} кг
- Тариф: {schema.tariff_name}
- Цена за кг: {schema.tariff_price_per_kg} ₽/кг

💰 Итоговая стоимость: {schema.total_price}₽
💳 Ссылка на оплату: [(перейти)]({schema.payment_url})
"""