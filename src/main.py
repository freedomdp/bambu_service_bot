#!/usr/bin/env python3
"""
Головний файл Telegram бота для сервісного центру Bambu Lab Україна
"""
import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application

from handlers import register_commands, register_conversation_handlers

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Головна функція для запуску бота"""
    # Завантажуємо змінні оточення
    load_dotenv()

    # Отримуємо токен бота
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN не встановлено в змінних оточення")

    # Створюємо додаток
    application = Application.builder().token(token).build()

    # Реєструємо обробники
    register_commands(application)
    register_conversation_handlers(application)

    # Запускаємо бота
    logger.info("Бот запущено...")
    application.run_polling()


if __name__ == '__main__':
    main()
