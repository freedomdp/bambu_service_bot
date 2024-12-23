from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from .utils import format_service_request
import logging
from keyboards.reply import (
    get_start_keyboard,
    get_printer_models_keyboard,
    get_plastic_types_keyboard,
    remove_keyboard
)
from config import ENGINEER_TELEGRAM_ID

logger = logging.getLogger(__name__)

from states.form_states import FormStates
from .utils import format_service_request, send_to_engineer, validate_phone

async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Початок заповнення форми.
    Запитує ПІБ користувача.
    """
    # Ініціалізуємо словник для збереження даних форми
    context.user_data['form_data'] = {}
    
    await update.message.reply_text(
        "📝 Почнемо заповнення заявки!\n\n"
        "Будь ласка, введіть ваше повне ПІБ:",
        reply_markup=remove_keyboard()
    )
    return FormStates.NAME

async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка введеного ПІБ та запит номера телефону.
    """
    name = update.message.text
    if len(name.split()) < 2:
        await update.message.reply_text(
            "⚠️ Будь ласка, введіть повне ПІБ (Прізвище та Ім'я обов'язково):"
        )
        return FormStates.NAME
    
    context.user_data['form_data']['name'] = name
    
    await update.message.reply_text(
        "📱 Введіть ваш номер телефону у форматі:\n"
        "+380XXXXXXXXX або 380XXXXXXXXX"
    )
    return FormStates.PHONE

async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка номера телефону та запит номера замовлення.
    """
    phone = update.message.text
    
    if not validate_phone(phone):
        await update.message.reply_text(
            "⚠️ Некоректний формат номера телефону.\n"
            "Будь ласка, введіть номер у форматі:\n"
            "+380XXXXXXXXX або 380XXXXXXXXX"
        )
        return FormStates.PHONE
    
    context.user_data['form_data']['phone'] = phone
    
    await update.message.reply_text(
        "🔢 Введіть номер замовлення, за яким ви купували принтер "
        "(якщо купували не у нас, просто напишіть 'немає'):"
    )
    return FormStates.ORDER_NUMBER

async def process_order_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка номера замовлення та перехід до вибору принтера.
    """
    order_number = update.message.text
    context.user_data['form_data']['order_number'] = order_number
    
    # Переходимо до вибору принтера
    await update.message.reply_text(
        "🖨️ Оберіть модель вашого принтера:",
        reply_markup=get_printer_models_keyboard()
    )
    return FormStates.PRINTER_MODEL  # Переходимо до вибору принтера, а не пластику

async def process_printer_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка вибору принтера та перехід до вибору пластику.
    """
    printer_model = update.message.text
    
    valid_models = [
        "X1C", "X1C Combo", "X1E",
        "P1P", "P1S", "P1S Combo",
        "A1", "A1 Combo", "A1 mini", "A1 mini Combo",
        "Інша модель"
    ]
    
    if printer_model not in valid_models:
        await update.message.reply_text(
            "⚠️ Будь ласка, оберіть модель принтера з клавіатури нижче:",
            reply_markup=get_printer_models_keyboard()
        )
        return FormStates.PRINTER_MODEL  # Залишаємось в стані вибору принтера
        
    # Зберігаємо модель принтера
    context.user_data['form_data']['printer_model'] = printer_model
    
    # Переходимо до вибору пластику
    await update.message.reply_text(
        "🎨 Вкажіть тип та бренд пластику, який використовуєте:",
        reply_markup=get_plastic_types_keyboard()
    )
    return FormStates.PLASTIC_TYPE  # Переходимо до стану вибору пластику

# Додаємо новий обробник для користувацької моделі
async def process_custom_printer_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка введеної користувачем моделі принтера.
    """
    if update.message.text == "⬅️ Назад":
        return await handle_back_button(update, context, FormStates.CUSTOM_PRINTER_MODEL)
        
    printer_model = update.message.text
    context.user_data['form_data']['printer_model'] = f"Інша модель: {printer_model}"
    
    await update.message.reply_text(
        "🎨 Вкажіть тип та бренд пластику, який використовуєте:",
        reply_markup=remove_keyboard()
    )
    return FormStates.PLASTIC_TYPE

async def process_plastic_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка вибору типу пластику та перехід до опису проблеми.
    """
    plastic_type = update.message.text
    valid_plastics = [
        "BambuLab PLA", "PLA інший бренд",
        "BambuLab PETG", "PETG інший бренд",
        "BambuLab TPU", "TPU інший бренд",
        "BambuLab ABS", "ABS інший бренд",
        "інший тип напишу у коментарі", "пропустити"
    ]
    
    if plastic_type not in valid_plastics:
        await update.message.reply_text(
            "⚠️ Будь ласка, оберіть тип пластику з клавіатури нижче:",
            reply_markup=get_plastic_types_keyboard()
        )
        return FormStates.PLASTIC_TYPE  # Залишаємось в стані вибору пластику

    if plastic_type == "інший тип напишу у коментарі":
        await update.message.reply_text(
            "Будь ласка, введіть тип та бренд пластику:",
            reply_markup=remove_keyboard()
        )
        return FormStates.PLASTIC_TYPE  # Залишаємось в стані вибору пластику
        
    # Зберігаємо тип пластику
    context.user_data['form_data']['plastic_type'] = plastic_type if plastic_type != "пропустити" else "Не вказано"
    
    # Переходимо до опису проблеми
    await update.message.reply_text(
        "❗ Опишіть проблему, з якою ви зіткнулися:\n\n"
        "Будь ласка, надайте якомога більше деталей.",
        reply_markup=remove_keyboard()
    )
    return FormStates.DESCRIPTION  # Переходимо до стану опису проблеми

async def process_custom_plastic_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка введеного користувачем типу пластику.
    """
    if update.message.text == "⬅️ Назад":
        return await handle_back_button(update, context, FormStates.CUSTOM_PLASTIC_TYPE)
        
    plastic_type = update.message.text
    context.user_data['form_data']['plastic_type'] = f"Інший тип: {plastic_type}"
    
    # Переходимо до опису проблеми
    await update.message.reply_text(
        "❗ Опишіть проблему, з якою ви зіткнулися:\n\n"
        "Будь ласка, надайте якомога більше деталей.",
        reply_markup=remove_keyboard()
    )
    return FormStates.DESCRIPTION

async def process_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка опису проблеми та запит фото.
    """
    try:
        if update.message.text == "⬅️ Назад":
            return await handle_back_button(update, context, FormStates.DESCRIPTION)
            
        description = update.message.text
        if len(description) < 10:
            await update.message.reply_text(
                "⚠️ Опис занадто короткий. Будь ласка, опишіть проблему детальніше:"
            )
            return FormStates.DESCRIPTION
        
        context.user_data['form_data']['description'] = description
        
        await update.message.reply_text(
            "📸 Надішліть фото, які демонструють проблему "
            "(до 10 фото).\n\n"
            "Після завершення відправки фото, натисніть 'Далі'",
            reply_markup=ReplyKeyboardMarkup([["Далі"]], resize_keyboard=True)
        )
        context.user_data['photos'] = []
        return FormStates.PHOTOS
        
    except Exception as e:
        logger.error(f"Error in process_description: {str(e)}")
        await update.message.reply_text(
            "😢 Сталася помилка при обробці вашого запиту.\n"
            "Будь ласка, спробуйте знову або зверніться до адміністратора."
        )
        return ConversationHandler.END

async def process_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка фото проблеми.
    """
    if update.message.photo:
        if not context.user_data.get('photos'):
            context.user_data['photos'] = []
            
        if len(context.user_data['photos']) >= 10:
            await update.message.reply_text(
                "⚠️ Досягнуто максимальну кількість фото (10)\n"
                "Натисніть 'Далі' для продовження",
                reply_markup=ReplyKeyboardMarkup([["Далі", "Пропустити"]], resize_keyboard=True)
            )
            return FormStates.PHOTOS
            
        # Зберігаємо фото
        file_id = update.message.photo[-1].file_id
        context.user_data['photos'].append(file_id)
        
        # Повідомлення про успішне додавання фото
        await update.message.reply_text(
            f"✅ Фото додано ({len(context.user_data['photos'])}/10)\n"
            "Можете додати ще фото або натисніть 'Далі'",
            reply_markup=ReplyKeyboardMarkup([["Далі", "Пропустити"]], resize_keyboard=True)
        )
        return FormStates.PHOTOS
        
    if update.message.text in ["Далі", "Пропустити"]:
        await update.message.reply_text(
            "📸 Тепер надішліть скріншоти налаштувань Bambu Studio.\n"
            "Після завершення натисніть 'Підтвердити'\n"
            "Або натисніть 'Пропустити', якщо не маєте скріншотів",
            reply_markup=ReplyKeyboardMarkup([["Підтвердити", "Пропустити"]], resize_keyboard=True)
        )
        context.user_data['settings_photos'] = []
        return FormStates.SETTINGS
    
    if not context.user_data.get('photos'):
        context.user_data['photos'] = []
        await update.message.reply_text(
            "📸 Надішліть фото, які демонструють проблему (до 10 фото).\n"
            "Після завершення натисніть 'Далі'\n"
            "Або натисніть 'Пропустити', якщо не маєте фото",
            reply_markup=ReplyKeyboardMarkup([["Далі", "Пропустити"]], resize_keyboard=True)
        )
    
    return FormStates.PHOTOS

async def process_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> FormStates:
    """
    Обробка фото налаштувань.
    """
    if update.message.photo:
        if not context.user_data.get('settings_photos'):
            context.user_data['settings_photos'] = []
            
        if len(context.user_data['settings_photos']) >= 10:
            await update.message.reply_text(
                "⚠️ Досягнуто максимальну кількість скріншотів (10)\n"
                "Натисніть 'Підтвердити' для продовження",
                reply_markup=ReplyKeyboardMarkup([["Підтвердити", "Пропустити"]], resize_keyboard=True)
            )
            return FormStates.SETTINGS
            
        # Зберігаємо фото
        file_id = update.message.photo[-1].file_id
        context.user_data['settings_photos'].append(file_id)
        
        # Повідомлення про успішне додавання скріншоту
        await update.message.reply_text(
            f"✅ Скріншот додано ({len(context.user_data['settings_photos'])}/10)\n"
            "Можете додати ще скріншоти або натиснути 'Підтвердити'",
            reply_markup=ReplyKeyboardMarkup([["Підтвердити", "Пропустити"]], resize_keyboard=True)
        )
        return FormStates.SETTINGS
        
    elif update.message.text in ["Підтвердити", "Пропустити"]:
        # Формуємо підсумок заявки для підтвердження
        form_data = context.user_data['form_data']
        summary = await format_service_request(form_data)
        
        await update.message.reply_text(
            f"📋 Перевірте дані вашої заявки:\n\n{summary}",
            reply_markup=ReplyKeyboardMarkup([["✅ Підтвердити", "❌ Скасувати"]], resize_keyboard=True)
        )
        return FormStates.CONFIRM
        
    # Якщо перше повідомлення в цьому стані
    if not context.user_data.get('settings_photos'):
        context.user_data['settings_photos'] = []
        await update.message.reply_text(
            "📸 Тепер надішліть скріншоти налаштувань Bambu Studio.\n"
            "Після завершення натисніть 'Підтвердити'\n"
            "Або натисніть 'Пропустити', якщо не маєте скріншотів",
            reply_markup=ReplyKeyboardMarkup([["Підтвердити", "Пропустити"]], resize_keyboard=True)
        )
    
    return FormStates.SETTINGS

async def process_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Фінальна обробка та відправка заявки інженеру.
    """
    try:
        if update.message.text == "✅ Підтвердити":
            # Відправляємо заявку інженеру
            form_data = context.user_data['form_data']
            await send_to_engineer(update, await format_service_request(form_data))
            
            # Відправляємо фото проблеми
            bot = context.bot
            if context.user_data.get('photos'):
                await bot.send_message(
                    ENGINEER_TELEGRAM_ID,
                    "📸 Фото проблеми:"
                )
                for photo_id in context.user_data['photos']:
                    try:
                        await bot.send_photo(ENGINEER_TELEGRAM_ID, photo_id)
                    except Exception as e:
                        logger.error(f"Error sending problem photo: {str(e)}")
            
            # Відправляємо фото налаштувань
            if context.user_data.get('settings_photos'):
                await bot.send_message(
                    ENGINEER_TELEGRAM_ID,
                    "🔧 Скріншоти налаштувань:"
                )
                for photo_id in context.user_data['settings_photos']:
                    try:
                        await bot.send_photo(ENGINEER_TELEGRAM_ID, photo_id)
                    except Exception as e:
                        logger.error(f"Error sending settings photo: {str(e)}")
            
            try:
                await update.message.reply_text(
                    "✅ Дякуємо! Вашу заявку прийнято.\n"
                    "Наш інженер розгляне її найближчим часом.",
                    reply_markup=get_start_keyboard()
                )
            except Exception as e:
                logger.error(f"Error sending final message: {str(e)}")
                await update.message.reply_text(
                    "✅ Дякуємо! Вашу заявку прийнято.\n"
                    "Наш інженер розгляне її найближчим часом."
                )
            
            return ConversationHandler.END
            
    except Exception as e:
        logger.error(f"Error in process_confirmation: {str(e)}")
        await update.message.reply_text(
            "✅ Вашу заявку було успішно відправлено, але виникла технічна помилка.\n"
            "Наш інженер все одно отримав ваше звернення та зв'яжеться з вами."
        )
        return ConversationHandler.END