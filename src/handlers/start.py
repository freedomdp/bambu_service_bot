# service_bot/src/handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.reply import get_start_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробник команди /start.
    Відправляє привітальне повідомлення та показує кнопку створення заявки.
    
    Args:
        update (Update): Об'єкт оновлення Telegram
        context (ContextTypes.DEFAULT_TYPE): Контекст бота
    """
    welcome_text = (
        "👋 Вітаю! Я бот сервісного центру Bambu Lab Україна.\n\n"
        "Для створення заявки на сервісне обслуговування натисніть кнопку '📝 Створити заявку' "
        "або використайте команду /new_request"
    )
    
    # Очищаємо дані попередніх заявок, якщо вони є
    if 'form_data' in context.user_data:
        context.user_data.clear()
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_start_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробник команди /help.
    Відправляє інформацію про можливості бота.
    """
    help_text = (
        "ℹ️ Доступні команди:\n\n"
        "/start - Почати роботу з ботом\n"
        "/new_request - Створити нову заявку\n"
        "/help - Отримати цю довідку\n"
        "/cancel - Скасувати поточну операцію\n\n"
        "При створенні заявки дотримуйтесь інструкцій бота. "
        "Вам потрібно буде надати:\n"
        "- ПІБ\n"
        "- Номер телефону\n"
        "- Номер замовлення (якщо є)\n"
        "- Модель принтера\n"
        "- Тип пластику\n"
        "- Опис проблеми\n"
        "- Фото проблеми\n"
        "- Фото налаштувань Bambu Studio"
    )
    
    await update.message.reply_text(help_text)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробник команди /cancel.
    Скасовує поточну операцію та очищає дані форми.
    """
    context.user_data.clear()
    
    await update.message.reply_text(
        "❌ Операцію скасовано. Щоб почати спочатку, використайте /start",
        reply_markup=get_start_keyboard()
    )