from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_main_keyboard() -> ReplyKeyboardMarkup:
	"""
	Повертає клавіатуру головного меню
	"""
	kb = [
		[
			KeyboardButton(text="🔧 Поломка"),
			KeyboardButton(text="🖨 Якість друку"),
			KeyboardButton(text="❓ Питання / Відповідь")
		]
	]
	return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def remove_keyboard() -> ReplyKeyboardRemove:
	"""
	Повертає об'єкт для видалення клавіатури
	"""
	return ReplyKeyboardRemove()
