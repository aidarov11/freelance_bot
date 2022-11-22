from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton('Показать задания')
btn2 = KeyboardButton('Добавить задание')
btn3 = KeyboardButton('Мои задания')
btn4 = KeyboardButton('Режим Модератора')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(btn1).row(btn2).row(btn3)

menu_kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb2.add(btn1).row(btn2).row(btn3).row(btn4)


other_btn = KeyboardButton('Другое')
cancel_btn = KeyboardButton('Отмена')


cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(cancel_btn)


category_btn1 = KeyboardButton('Разработка сайтов')
category_btn2 = KeyboardButton('Дизайн и Арт')
category_btn3 = KeyboardButton('Тексты')
category_btn4 = KeyboardButton('Программирование')
category_btn5 = KeyboardButton('Аудио/Видео')
category_btn6 = KeyboardButton('Разработка игр')
category_btn7 = KeyboardButton('Реклама и Маркетинг')
category_btn8 = KeyboardButton('Аутсорсинг и консалтинг')
category_btn9 = KeyboardButton('Анимация и флеш')
category_btn10 = KeyboardButton('3D Графика')
category_btn11 = KeyboardButton('Фотография')
category_btn12 = KeyboardButton('Инжиниринг')
category_btn13 = KeyboardButton('Архитектура/Интерьер')
category_btn14 = KeyboardButton('Оптимизация (SEO)')
category_btn15 = KeyboardButton('Полиграфия')
category_btn16 = KeyboardButton('Обучение и консультации')
category_btn17 = KeyboardButton('Менеджмент')
category_btn18 = KeyboardButton('Мобильные приложения')

categories_kb = ReplyKeyboardMarkup(resize_keyboard=True)
categories_kb.add(category_btn1, category_btn2, category_btn3, category_btn4, category_btn5, category_btn6, category_btn7, category_btn8, category_btn9, category_btn10, category_btn11, category_btn12, category_btn13, category_btn14, category_btn15, category_btn16, category_btn17, category_btn18).row(other_btn).row(cancel_btn)