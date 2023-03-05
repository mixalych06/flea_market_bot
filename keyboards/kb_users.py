from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyword: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

button_user_ads: KeyboardButton = KeyboardButton('Мои объявления')
button_add_ad: KeyboardButton = KeyboardButton('📌Подать объявление📌')

button_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyword.add(button_user_ads, button_add_ad).add(button_help)




