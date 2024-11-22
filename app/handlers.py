from aiogram import types, F, Router
from aiogram.filters import Command
import app.keyboards as kb
import sqlite3
from datetime import datetime, timedelta
from config import ADMIN_IDS
from database.database_manager import database_connection

router = Router()

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    welcome_text = f"Добро пожаловать, {message.from_user.first_name}! Выберите пункт меню!"
    await message.answer(welcome_text, reply_markup=kb.main_keyboard)

@router.message(lambda message: message.text == "Подробная информация")
async def send_info(message: types.Message):
    info_text = "Здесь будет подробная информация о вашем боте."
    await message.answer(info_text, reply_markup=kb.main_keyboard)


@router.message(lambda message:  message.text == "Анкеты")
async def show_surveys(message: types.Message):
    with database_connection as cursor:
        cursor.execute("SELECT * FROM survey WHERE user_ip = ?", (message.from_user.id,))
        surveys = cursor.fetchall()


    
    if surveys:
        for survey in surveys:
            checked_status = "Проверено" if survey[6] else "Не проверено"
            approved_status = "Одобрено, " if survey[7] else "Не одобрено" if survey[6] else ""
            
            comment = survey[8] if survey[8] else "Нет комментария"
            
            response = (f"Имя: {survey[1]}, "
                        f"Количество людей: {survey[2]}, "
                        f"Возраст: {survey[3]}, "
                        f"Время: {survey[4]}, "
                        f"Статус: {checked_status}, "
                        f"{approved_status}"
                        f"Комментарий: {comment}")
            
            await message.answer(response)  
    else:
        await message.answer("У вас нет анкет.")


@router.message(Command(commands=['admin_panel']))
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.reply("Добро пожаловать в панель администратора!", reply_markup=kb.admin_keyboard)
    else:
        await message.reply(message.from_user.id)


from aiogram import types
import sqlite3

@router.message(lambda message: message.text == "Ожидание")
async def checked_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        with database_connection as cursor:
            cursor.execute("SELECT * FROM survey WHERE checked = 0")
            checked = cursor.fetchall()

        
        if checked:
            await message.answer("Найдены следующие записи:\n")
            for record in checked:
                approve_button = types.InlineKeyboardButton(text="Одобрено", callback_data=f"approve_{record[0]}")
                reject_button = types.InlineKeyboardButton(text="Отказано", callback_data=f"reject_{record[0]}")
                
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[approve_button, reject_button]])

                await message.answer(
                    f"ID: {record[0]}, Имя: {record[1]}, Количество людей: {record[2]}, "
                    f"Возраст: {record[3]}, Время: {record[4]}, Комментарий: {record[8]}\n",
                    reply_markup=keyboard 
                )
        else:
            await message.answer("Нет записей с состоянием 'Ожидание'.")

@router.callback_query(lambda message: message.data.startswith('approve_'))
async def process_approve(callback_query: types.CallbackQuery):
    record_id = callback_query.data.split('_')[1]
    
    with database_connection as cursor:
        cursor.execute("UPDATE survey SET checked = 1, approved = 1 WHERE id = ?", (record_id,))

    
    await callback_query.answer(f"Запись {record_id} одобрена.")

@router.callback_query(lambda message: message.data.startswith('reject_'))
async def process_reject(callback_query: types.CallbackQuery):
    record_id = callback_query.data.split('_')[1]
    
    with database_connection as cursor:
        cursor.execute("UPDATE survey SET checked = 1, approved = 0 WHERE id = ?", (record_id,)) 

    await callback_query.answer(f"Запись {record_id} отклонена.")


@router.message(lambda message: message.text == "Одобренные")
async def approved_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        with database_connection as cursor:
            cursor.execute("SELECT * FROM survey WHERE checked = 1")
            approved = cursor.fetchall()
        
        
        if approved:
            await message.answer("Найдены следующие одобренные записи:\n")
            for record in approved:
                await message.answer(
                    f"ID: {record[0]}, Имя: {record[1]}, Количество людей: {record[2]}, "
                    f"Возраст: {record[3]}, Время: {record[4]}, Комментарий: {record[8]}\n"
                )
        else:
            await message.answer("Нет записей с состоянием 'Одобрено'.")

@router.message(lambda message: message.text == "Удаление старых запией")
async def delete_old_records(message: types.Message):
    with database_connection as cursor:
        month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        DELETE FROM survey WHERE time < ?;  -- Убедитесь, что имя столбца корректно
        ''', (month_ago,))
        
        cursor.execute('VACUUM;')

    await message.answer("Удаление старых запией закончено")