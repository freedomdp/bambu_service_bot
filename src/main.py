import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import config, logger
from models.dialog import DialogManager
from models.user import UserManager
from services.message_service import MessageService
from middlewares.setup_middlewares import setup_middlewares
from routers import breakdown, common

async def main() -> None:
    """Головна функція запуску бота"""
    # Налаштування логування
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ініціалізація бота та диспетчера
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=config.TOKEN, default=default)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Ініціалізація сервісів
    dialog_manager = DialogManager()
    user_manager = UserManager()
    message_service = MessageService(bot)
    
    # Налаштування middleware
    setup_middlewares(dp, dialog_manager, user_manager, message_service)
    
    # Реєстрація роутерів
    dp.include_router(common.router)
    dp.include_router(breakdown.router)
    
    logger.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


