from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подробная информация")],
        [KeyboardButton(text="Заполнение анкеты")],
        [KeyboardButton(text="Анкеты")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери пункт меню."
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Одобренные")],
        [KeyboardButton(text="Ожидание")],
        [KeyboardButton(text="Удаление старых запией")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери пункт меню."
)