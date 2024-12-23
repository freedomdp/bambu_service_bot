# service_bot/src/keyboards/reply.py
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_start_keyboard() -> ReplyKeyboardMarkup:
    """
    Створює стартову клавіатуру з однією кнопкою.
    """
    keyboard = [[KeyboardButton("📝 Створити заявку")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def add_back_button(keyboard_buttons: list) -> list:
    """
    Додає кнопку 'Назад' до існуючої клавіатури.
    """
    return keyboard_buttons + [["⬅️ Назад"]] 

def get_printer_models_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавіатура з повним переліком моделей принтерів Bambu Lab у 3 колонки.
    """
    keyboard = [
        # Серія X
        [
            KeyboardButton("X1C"),
            KeyboardButton("X1C Combo"),
            KeyboardButton("X1E"),
        ],
        # Серія P
        [
            KeyboardButton("P1P"),
            KeyboardButton("P1S"),
            KeyboardButton("P1S Combo"),
        ],
        # Серія A
        [
            KeyboardButton("A1"),
            KeyboardButton("A1 Combo"),
            KeyboardButton("A1 mini"),
        ],
        [
            KeyboardButton("A1 mini Combo"),
            KeyboardButton("Інша модель"),
        ]
    ]
    return ReplyKeyboardMarkup(add_back_button(keyboard), resize_keyboard=True)

def get_plastic_types_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавіатура з типами пластику у 2 колонки.
    """
    keyboard = [
        ["BambuLab PLA", "PLA інший бренд"],
        ["BambuLab PETG", "PETG інший бренд"],
        ["BambuLab TPU", "TPU інший бренд"],
        ["BambuLab ABS", "ABS інший бренд"],
        ["інший тип напишу у коментарі", "пропустити"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавіатура для підтвердження даних заявки.
    """
    keyboard = [
        [KeyboardButton("✅ Підтвердити")],
        [KeyboardButton("❌ Скасувати")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def remove_keyboard() -> ReplyKeyboardRemove:
    """
    Прибирає клавіатуру у користувача.
    """
    return ReplyKeyboardRemove()