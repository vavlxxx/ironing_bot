def format_phone_number(phone):
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

🔗 **ID в CRM:** `{order.amocrm_lead_id or 'Не привязан'}`

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
