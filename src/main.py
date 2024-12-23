# service_bot/src/main.py
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from config import TELEGRAM_TOKEN
from handlers.start import start_command, help_command, cancel_command
from handlers.form import (
    start_form,
    process_name,
    process_phone,
    process_order_number,
    process_printer_model,
    process_custom_printer_model,
    process_plastic_type,
    process_custom_plastic_type,  
    process_description,
    process_photos,
    process_settings,
    process_confirmation
)
from states.form_states import FormStates

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Обробник помилок."""
    logger.error(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text(
            "😢 Сталася помилка при обробці вашого запиту.\n"
            "Будь ласка, спробуйте знову або зверніться до адміністратора."
        )

def main():
    """Головна функція запуску бота."""
    # Створюємо application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Створюємо ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_command),
            MessageHandler(filters.Regex('^📝 Створити заявку$'), start_form)
        ],
        states={
            FormStates.NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_name)
            ],
            FormStates.PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_phone)
            ],
            FormStates.ORDER_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_order_number)
            ],
            FormStates.PRINTER_MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_printer_model)
            ],
            FormStates.CUSTOM_PRINTER_MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_custom_printer_model)
            ],
            FormStates.PLASTIC_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_plastic_type)
            ],
            FormStates.CUSTOM_PLASTIC_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_custom_plastic_type)
            ],
            FormStates.DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_description)
            ],
            FormStates.PHOTOS: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, process_photos)
            ],
            FormStates.SETTINGS: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, process_settings)
            ],
            FormStates.CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_confirmation)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )

    # Додаємо обробники
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Додаємо обробник помилок
    application.add_error_handler(error_handler)

    # Запускаємо бота
    application.run_polling()

if __name__ == '__main__':
    main()