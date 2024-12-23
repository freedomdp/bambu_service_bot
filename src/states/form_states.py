# service_bot/src/states/form_states.py
from enum import Enum, auto

class FormStates(Enum):
    """
    Стани форми заявки.
    Використовуються для відстеження прогресу заповнення форми користувачем.
    """
    NAME = auto()                   # 2. ПІБ
    PHONE = auto()                  # 3. Телефон
    ORDER_NUMBER = auto()           # 4. Номер замовлення
    PRINTER_MODEL = auto()          # 5. Вибір моделі принтера
    CUSTOM_PRINTER_MODEL = auto()   # 5.1 Введення іншої моделі принтера
    PLASTIC_TYPE = auto()           # 6. Вибір типу пластику
    CUSTOM_PLASTIC_TYPE = auto()    # 6.1 Введення іншого типу пластику
    DESCRIPTION = auto()            # 7. Опис проблеми
    PHOTOS = auto()                 # 8. Фото проблеми
    SETTINGS = auto()               # 9. Скріншоти налаштувань
    CONFIRM = auto()                # 10. Підтвердження заявки