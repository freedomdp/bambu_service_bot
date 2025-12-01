from telegram import Update
from telegram.ext import ContextTypes
from ..handlers.conversation import (
    WAITING_PRINTER_MODEL,
    WAITING_FILAMENT_TYPE,
    WAITING_FILAMENT_MANUFACTURER,
    WAITING_PHOTOS,
    WAITING_MODEL_FILE,
    WAITING_DESCRIPTION,
    CONFIRMING,
    ConversationHandler,
    get_printer_model_callback,
    get_filament_type_callback,
    get_filament_manufacturer_callback,
    skip_photos,
    skip_model_file,
    cancel,
    active_applications,
)
from ..keyboards.inline import (
    get_printer_model_keyboard,
    get_filament_type_keyboard,
    get_filament_manufacturer_keyboard,
    get_skip_keyboard,
    get_confirm_keyboard,
    PRINTER_MODELS,
    FILAMENT_TYPES,
    FILAMENT_MANUFACTURERS,
)
import os


async def handle_printer_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обробка вибору моделі принтера"""
    return await get_printer_model_callback(update, context)


async def handle_filament_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обробка вибору типу філаменту"""
    return await get_filament_type_callback(update, context)


async def handle_filament_manufacturer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обробка вибору виробника філаменту"""
    return await get_filament_manufacturer_callback(update, context)


async def handle_skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обробка пропуску опціональних полів"""
    query = update.callback_query
    user_id = update.effective_user.id

    if user_id not in active_applications:
        await query.answer("❌ Помилка. Будь ласка, почніть з команди /new_application")
        return ConversationHandler.END

    # Визначаємо, яке поле пропускаємо на основі контексту
    # Це спрощена версія - в реальному проекті краще використовувати окремі callback_data
    current_state = context.user_data.get('conversation_state')

    if query.message.text and 'номер замовлення' in query.message.text.lower():
        # Пропускаємо номер замовлення
        from ..keyboards.inline import get_printer_model_keyboard
        await query.answer()
        await query.edit_message_text(
            "Оберіть <b>модель вашого 3D-принтера</b>:",
            parse_mode='HTML',
            reply_markup=get_printer_model_keyboard()
        )
        return WAITING_PRINTER_MODEL

    elif query.message.text and ('фото' in query.message.text.lower() or 'відео' in query.message.text.lower()):
        # Пропускаємо фото
        return await skip_photos(update, context)

    elif query.message.text and '3d модель' in query.message.text.lower():
        # Пропускаємо 3D модель
        return await skip_model_file(update, context)

    await query.answer()
    return ConversationHandler.END


async def handle_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Підтвердження та відправка заявки інженеру"""
    query = update.callback_query
    user_id = update.effective_user.id

    if user_id not in active_applications:
        await query.answer("❌ Помилка. Заявка не знайдена.")
        return ConversationHandler.END

    app = active_applications[user_id]

    if not app.is_complete():
        await query.answer("❌ Заявка не повна. Будь ласка, заповніть всі обов'язкові поля.")
        return CONFIRMING

    # Отримуємо ID інженера з змінних оточення
    engineer_id = os.getenv('ENGINEER_TELEGRAM_ID')

    if not engineer_id:
        await query.answer("❌ Помилка конфігурації. Інженер не налаштований.")
        return ConversationHandler.END

    try:
        engineer_id = int(engineer_id)

        # Відправляємо заявку інженеру
        message_text = app.to_message()

        # Відправляємо текст заявки
        await context.bot.send_message(
            chat_id=engineer_id,
            text=message_text,
            parse_mode='HTML'
        )

        # Відправляємо фото/відео якщо є
        if app.photos:
            media_group = []
            for photo_id in app.photos[:10]:  # Telegram дозволяє до 10 файлів в групі
                media_group.append({
                    'type': 'photo',
                    'media': photo_id
                })

            # Розділяємо на групи по 10 файлів
            for i in range(0, len(media_group), 10):
                group = media_group[i:i+10]
                await context.bot.send_media_group(
                    chat_id=engineer_id,
                    media=group
                )

        # Відправляємо 3D модель якщо є
        if app.model_file:
            await context.bot.send_document(
                chat_id=engineer_id,
                document=app.model_file,
                caption="3D модель від клієнта"
            )

        # Підтверджуємо користувачу
        await query.answer("✅ Заявка успішно відправлена!")
        await query.edit_message_text(
            "✅ <b>Заявка успішно відправлена!</b>\n\n"
            "Наш спеціаліст надасть вам відповідь протягом до 2 робочих днів "
            "на вказаний вами email адресу.\n\n"
            "Дякуємо за звернення! 🙏",
            parse_mode='HTML'
        )

        # Видаляємо заявку з активних
        del active_applications[user_id]

        return ConversationHandler.END

    except Exception as e:
        await query.answer(f"❌ Помилка при відправці заявки: {str(e)}")
        return CONFIRMING


# Callback handlers реєструються всередині ConversationHandler
# Ця функція більше не використовується
def register_callback_handlers(application):
    """Реєстрація обробників callback-запитів (не використовується)"""
    pass
