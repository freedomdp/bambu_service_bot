# service_bot/src/handlers/utils.py
from telegram import Update
from telegram.ext import ContextTypes
from typing import Union
from telegram import ReplyKeyboardMarkup
from states.form_states import FormStates
from keyboards.reply import get_printer_models_keyboard
from datetime import datetime
import pytz
from config import ENGINEER_TELEGRAM_ID

async def format_service_request(data: dict) -> str:
    """
    Форматує дані заявки для відправки інженеру.
    
    Args:
        data (dict): Словник з даними заявки
    
    Returns:
        str: Відформатований текст заявки
    """
    # Отримуємо поточний час у київському часовому поясі
    kyiv_tz = pytz.timezone('Europe/Kiev')
    current_time = datetime.now(kyiv_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
🆕 Нова заявка на сервіс

⏰ Дата та час: {current_time} (Київ)

👤 Клієнт: {data.get('name')}
📞 Телефон: {data.get('phone')}
🔢 Номер замовлення: {data.get('order_number', 'Не вказано')}

🖨️ Принтер: {data.get('printer_model')}
🎨 Пластик: {data.get('plastic_type')}

❗ Опис проблеми:
{data.get('description')}

📎 Фото та налаштування додаються окремими повідомленнями
"""

async def send_to_engineer(update: Update, text: str) -> None:
    """
    Відправляє повідомлення інженеру сервісного центру.
    
    Args:
        update (Update): Об'єкт оновлення Telegram
        text (str): Текст для відправки
    """
    bot = update.get_bot()
    await bot.send_message(
        chat_id=ENGINEER_TELEGRAM_ID,
        text=text,
        parse_mode='HTML'
    )

async def validate_phone(phone: str) -> bool:
    """
    Перевіряє правильність формату номера телефону.
    
    Args:
        phone (str): Номер телефону для перевірки
    
    Returns:
        bool: True якщо формат правильний, False якщо ні
    """
    # Видаляємо всі символи крім цифр
    cleaned_phone = ''.join(filter(str.isdigit, phone))
    # Перевіряємо довжину та починається з 380
    return len(cleaned_phone) == 12 and cleaned_phone.startswith('380')

async def handle_back_button(update: Update, context: ContextTypes.DEFAULT_TYPE, current_state: FormStates) -> FormStates:
    """
    Обробляє натискання кнопки 'Назад'.
    """
    state_flow = {
        FormStates.PHONE: (FormStates.NAME, "Будь ласка, введіть ваше повне ПІБ:"),
        FormStates.ORDER_NUMBER: (FormStates.PHONE, "Введіть ваш номер телефону:"),
        FormStates.PRINTER_MODEL: (FormStates.ORDER_NUMBER, "Введіть номер замовлення:"),
        FormStates.PLASTIC_TYPE: (FormStates.PRINTER_MODEL, "Оберіть модель вашого принтера:"),
        FormStates.DESCRIPTION: (FormStates.PLASTIC_TYPE, "Вкажіть тип та бренд пластику:"),
        FormStates.PHOTOS: (FormStates.DESCRIPTION, "Опишіть проблему:"),
        FormStates.SETTINGS: (FormStates.PHOTOS, "Надішліть фото проблеми:"),
    }

    if current_state in state_flow:
        prev_state, message = state_flow[current_state]
        await update.message.reply_text(
            message,
            reply_markup=get_keyboard_for_state(prev_state)
        )
        return prev_state
    
    return current_state

def get_keyboard_for_state(state: FormStates) -> Union[ReplyKeyboardMarkup, None]:
    """
    Повертає відповідну клавіатуру для конкретного стану.
    """
    if state == FormStates.PRINTER_MODEL:
        return get_printer_models_keyboard()
    # Додайте інші клавіатури для інших станів за потреби
    return None