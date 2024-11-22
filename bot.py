from aiogram import Bot, Dispatcher
import logging
import asyncio
from config import *
from app.handlers import router
from app.form import form_router
from database.database_manager import init_database 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    dp.include_router(form_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    init_database()
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")
