#!/usr/bin/env python3
"""
Головний файл Telegram бота для сервісного центру Bambu Lab Україна
"""
import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application

from handlers import register_commands, register_conversation_handlers
from services import MediaStorage, ErrorHandler, ReminderService
from services.context import (
    set_media_storage, set_error_handler, set_reminder_service
)

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
    
    # Инициализируем сервисы
    media_storage = MediaStorage(
        storage_path=os.getenv('MEDIA_STORAGE_PATH', './media'),
        base_url=os.getenv('BASE_URL', 'http://localhost:8000')
    )
    
    error_handler = ErrorHandler()
    reminder_service = ReminderService(bot=application.bot)
    
    # Устанавливаем сервисы в контекст для доступа из обработчиков
    set_media_storage(media_storage)
    set_error_handler(error_handler)
    set_reminder_service(reminder_service)
    
    # Реєструємо обробники
    register_commands(application)
    register_conversation_handlers(application)
    
    # Регистрируем глобальный обработчик ошибок
    application.add_error_handler(error_handler.handle_error)
    
    # Запускаємо сервіс напоминаний
    reminder_service.start()

    # Запускаємо бота
    logger.info("Бот запущено...")
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
    finally:
        # Останавливаем сервисы
        reminder_service.stop()
        logger.info("Бот остановлен")


if __name__ == '__main__':
    main()
