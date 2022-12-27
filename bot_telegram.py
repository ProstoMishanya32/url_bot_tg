import aiogram
from create_bot import dp, bot
from aiogram import executor
import asyncio
from handlers import user, admin, url
from modules import sqlite_logic

async def on_startup(_):
    print('Бот успешно запустился')
    sqlite_logic.start()

user.registry_handlers_user(dp)
admin.registry_handlers_admin(dp)
url.registry_handlers_url(dp)
if __name__  == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
