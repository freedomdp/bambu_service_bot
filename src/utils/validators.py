"""
Валідатори для перевірки введених даних
"""
import re
from typing import Tuple

def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Валидация номера телефона
    Returns: (is_valid, cleaned_phone or error_message)
    """
    # Удаляем все пробелы и тире
    cleaned_phone = re.sub(r'[\s-]', '', phone)
    
    # Проверяем формат +380XXXXXXXXX
    if not cleaned_phone.startswith('+380'):
        return False, "❗️ Номер телефону має починатися з +380"
    
    # Проверяем длину (должно быть 13 символов с учетом +)
    if len(cleaned_phone) != 13:
        return False, "❗️ Введіть будь ласка номер тільки у форматі +380XXXXXXXXX"
    
    # Проверяем, что после +380 идут только цифры
    if not cleaned_phone[4:].isdigit():
        return False, "❗️ Після +380 мають бути тільки цифри"
    
    return True, cleaned_phone

class PrinterModelValidator:
    """
    Клас для валідації моделі принтера
    """
    VALID_MODELS = {'A1', 'A1 mini', 'P1P', 'P1S', 'X1C', 'X1E'}
    
    @staticmethod
    def validate(model: str) -> Tuple[bool, str]:
        """
        Перевіряє правильність введення моделі принтера
        Повертає: (успіх, результат)
        """
        if model == 'Пропустити':
            return True, None
        elif model == 'Інша модель':
            return True, 'other'
        elif model in PrinterModelValidator.VALID_MODELS:
            return True, model
        else:
            return False, "❌ Будь ласка, оберіть модель зі списку або введіть точну назву моделі"


class PhoneValidator:
    """
    Клас для валідації номера телефону
    """
    @staticmethod
    def validate(phone: str) -> Tuple[bool, str]:
        """
        Перевіряє правильність введення номера телефону
        Повертає: (успіх, результат)
        """
        return validate_phone(phone)




class IssueDescriptionValidator:
    """
    Клас для валідації опису проблеми
    """
    MIN_LENGTH = 10
    
    @staticmethod
    def validate(description: str) -> Tuple[bool, str]:
        """
        Перевіряє правильність опису проблеми
        Повертає: (успіх, результат/повідомлення про помилку)
        """
        if len(description.strip()) < IssueDescriptionValidator.MIN_LENGTH:
            return False, "❌ Опис проблеми занадто короткий. Будь ласка, опишіть проблему детальніше (мінімум 10 символів)"
        return True, description.strip()