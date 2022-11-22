from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton('Активные задания')
btn2 = KeyboardButton('Ожидают проверки')
btn3 = KeyboardButton('Сделать рассылку')
btn4 = KeyboardButton('Список модераторов')
btn5 = KeyboardButton('Добавить модератора')
btn6 = KeyboardButton('Выйти')

moderator_kb = ReplyKeyboardMarkup(resize_keyboard=True)
moderator_kb.row(btn1, btn2).row(btn3, btn4).add(btn5).add(btn6)


cancel_mailing_btn = KeyboardButton('Отменить рассылку')

cancel_mailing_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_mailing_kb.add(cancel_mailing_btn)


cancel_add_moderator_btn = KeyboardButton('Отменить добавление модератора')

cancel_add_moderator_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_add_moderator_kb.add(cancel_add_moderator_btn)