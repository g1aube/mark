from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_admin_sender = InlineKeyboardMarkup()
keyboard_admin_sender_button1 = InlineKeyboardButton(text='Вернуть обратно', callback_data='back_response')
keyboard_admin_sender_button2 = InlineKeyboardButton(text='Обработать', callback_data='send_response')
keyboard_admin_sender.add(keyboard_admin_sender_button1)
keyboard_admin_sender.add(keyboard_admin_sender_button2)

keyboard_language = InlineKeyboardMarkup()
keyboard_language_button1 = InlineKeyboardButton(text='Русский 🇷🇺', callback_data='ru_lg')
keyboard_language_button2 = InlineKeyboardButton(text='English 🇺🇸', callback_data='en_lg')
keyboard_language_button3 = InlineKeyboardButton(text='中国 🇨🇳', callback_data='cn_lg')
keyboard_language.add(keyboard_language_button2)
keyboard_language.add(keyboard_language_button1)
keyboard_language.add(keyboard_language_button3)

# Кнопка для пользователей чтобы они могли сделать запрос

keyboard_response_user_cn = InlineKeyboardMarkup()
keyboard_response_user_cn_button1 = InlineKeyboardButton(text='請單擊填充', callback_data='start_response')
keyboard_response_user_cn.add(keyboard_response_user_cn_button1)

keyboard_response_user_en = InlineKeyboardMarkup()
keyboard_response_user_en_button1 = InlineKeyboardButton(text='Fill', callback_data='start_response')
keyboard_response_user_en.add(keyboard_response_user_en_button1)

keyboard_response_user_ru = InlineKeyboardMarkup()
keyboard_response_user_ru_button = InlineKeyboardButton(text='Заполнить', callback_data='start_response')
keyboard_response_user_ru.add(keyboard_response_user_ru_button)

