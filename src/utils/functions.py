

from utils.exceptions import InvalidPhoneNumberException


def _format_phone_number(phone):
    if not phone:
        return None
    digits_only = "".join(char for char in phone if char.isdigit())
    if len(digits_only) < 10:
        return None
    if len(digits_only) == 10:
        return "7" + digits_only
    elif len(digits_only) == 11:
        if digits_only.startswith("8"):
            return "7" + digits_only[1:]
        elif digits_only.startswith("7"):
            return digits_only
        else:
            return digits_only
    else:
        return digits_only
    

def parse_phone_number(message):
    raw_phone = message.text.strip() if message.contact is None else message.contact.phone_number
    phone = _format_phone_number(raw_phone)
    if not phone or not phone.startswith("7"):
        raise InvalidPhoneNumberException
    return f"+{phone}"


def format_order_message(order) -> str:
    """Форматирует заказ для красивого отображения в Telegram"""
    created_date = "Не указана"
    if order.created_at:
        created_date = order.created_at.strftime("%d.%m.%Y в %H:%M")
    
    tariff_display = order.tariff_name or "Стандартный тариф"
    price_display = f"{order.total_price:,.0f}" if order.total_price % 1 == 0 else f"{order.total_price:,.2f}"
    weight_display = f"{order.total_weight_kg:.2f}".rstrip('0').rstrip('.')
    
    message = f"""
🧺 **Заказ #{order.order_number}**

📦 **Детали заказа:**
⚖️ Общий вес: `{weight_display} кг`
💰 Итоговая стоимость: `{price_display} ₽`
📋 Тариф: `{tariff_display}`

📅 **Дата создания:** {created_date}

🔗 **Ссылка на оплату:** `{order.payment_url or 'Отсутствует'}`

───────────────────────
"""
    
    return message

def format_orders_list(orders) -> str:
    
    if not orders:
        return "📭 У вас пока нет заказов"
    
    header = f"📝 **Ваши заказы** ({len(orders)} шт.):\n\n"
    
    formatted_orders = []
    for i, order in enumerate(orders, 1):
        formatted_orders.append(format_order_message(order))
    
    result = header + "\n".join(formatted_orders)
    
    if len(orders) > 3:
        result += f"\n💡 *Показано {len(orders)} заказов*"
    
    return result
