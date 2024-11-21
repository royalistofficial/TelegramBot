from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
from app.handlers import router
import sqlite3

def save_to_db(name, number_of_people, age, time, comment, user_ip):
    conn = sqlite3.connect('db/mydb.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO survey (name, number_of_people, age, time, comment, user_ip)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, number_of_people, age, time, comment, user_ip))
    
    conn.commit()
    conn.close()

class Form(StatesGroup):
    name = State()
    number_of_people = State() 
    age = State()               
    time = State() 
    comment = State()            


@router.message(lambda message: message.text == "Заполнение анкеты")
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Введите ваше имя:")

@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.number_of_people)
    await message.answer("Введите количество людей:")

@router.message(Form.number_of_people)
async def process_number_of_people(message: types.Message, state: FSMContext):
    try:
        number_of_people = int(message.text)
        await state.update_data(number_of_people=number_of_people)
        await state.set_state(Form.age)
        await message.answer("Введите ваш возраст:")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

@router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(Form.time)
        await message.answer("Введите время (например, 14:30):")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст.")

@router.message(Form.time)
async def process_time(message: types.Message, state: FSMContext):
    datetime_input = message.text
    try:
        datetime.strptime(datetime_input, "%d.%m.%Y %H:%M")
        await state.update_data(time=datetime_input)
        await state.set_state(Form.comment)
        await message.answer("Введите комментарий (необязательно):")
    except ValueError:
        await message.answer("Пожалуйста, введите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ.")

@router.message(Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    
    data = await state.get_data()
    save_to_db(data['name'], data['number_of_people'], data['age'], data['time'], comment, message.from_user.id)
        
    await message.answer("Спасибо за заполнение анкеты!")
    await state.clear()
