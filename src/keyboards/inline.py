from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Моделі принтерів Bambu Lab
PRINTER_MODELS = [
    "Bambu Lab X1 Carbon",
    "Bambu Lab X1",
    "Bambu Lab P1S",
    "Bambu Lab P1P",
    "Bambu Lab A1 mini",
    "Bambu Lab A1",
    "Інша модель",
]

# Типи філаменту
FILAMENT_TYPES = [
    "PLA",
    "PETG",
    "ABS",
    "ASA",
    "TPU",
    "PA (Nylon)",
    "PC (Polycarbonate)",
    "PP (Polypropylene)",
    "PVA",
    "PET",
    "Інший тип",
]

# Виробники філаменту
FILAMENT_MANUFACTURERS = [
    "Bambu Lab",
    "Polymaker",
    "eSun",
    "Sunlu",
    "Overture",
    "HATCHBOX",
    "Prusament",
    "Інший виробник",
]


def get_printer_model_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для вибору моделі принтера"""
    buttons = [
        [InlineKeyboardButton(model, callback_data=f"printer_{i}")]
        for i, model in enumerate(PRINTER_MODELS)
    ]
    return InlineKeyboardMarkup(buttons)


def get_filament_type_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для вибору типу філаменту"""
    buttons = [
        [InlineKeyboardButton(filament_type, callback_data=f"filament_type_{i}")]
        for i, filament_type in enumerate(FILAMENT_TYPES)
    ]
    return InlineKeyboardMarkup(buttons)


def get_filament_manufacturer_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для вибору виробника філаменту"""
    buttons = [
        [InlineKeyboardButton(manufacturer, callback_data=f"filament_man_{i}")]
        for i, manufacturer in enumerate(FILAMENT_MANUFACTURERS)
    ]
    return InlineKeyboardMarkup(buttons)


def get_skip_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура з кнопкою 'Пропустити'"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭️ Пропустити", callback_data="skip")]
    ])


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для підтвердження заявки"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Підтвердити", callback_data="confirm"),
            InlineKeyboardButton("❌ Скасувати", callback_data="cancel")
        ]
    ])
