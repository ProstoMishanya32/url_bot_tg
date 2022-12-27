import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from configs.text import messagetext, buttonstext, errortext
from modules import keyboard, json_logic,sqlite_logic
from handlers import admin, url

class URL(StatesGroup):
    message = State()

async def start(message: types.Message, state: FSMContext):
        await bot.send_message(message.from_user.id, messagetext['start_user'], parse_mode=types.ParseMode.HTML)
        await URL.message.set()

async def admin_start(message: types.Message):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            await bot.send_message(message.from_user.id, messagetext['start'], parse_mode=types.ParseMode.HTML, reply_markup = keyboard.button_1)


async def url_send(message: types.Message, state: FSMContext):
    try:
        admins = await json_logic.get_admins()
        int(message.text)
        text, check = await sqlite_logic.get_user_url(message.text)
        if check == False:
            await bot.send_message(message.from_user.id, errortext['url_remove_code'], parse_mode=types.ParseMode.HTML)
            if message.from_user.id in admins:
                await state.finish()
            else:
                await URL.message.set()
        else:
            await bot.send_message(message.from_user.id, text, parse_mode=types.ParseMode.HTML)
            if message.from_user.id in admins:
                await state.finish()
            else:
                await URL.message.set()

    except ValueError:
        await bot.send_message(message.from_user.id, errortext['error_not_int'], parse_mode=types.ParseMode.HTML)
        if message.from_user.id in admins:
            await state.finish()
        else:
            await URL.message.set()




async def menu(message: types.Message, state: FSMContext):
    admins = await json_logic.get_admins()
    if message.chat.type == "private":
        if message.from_user.id in admins:
            if message.text == buttonstext['add_admin']:
                await bot.send_message(message.from_user.id, messagetext['add_admin'], reply_markup=keyboard.button_2, parse_mode=types.ParseMode.HTML)
                await admin.Add_admin.message.set()
            elif message.text == buttonstext['remove_admin']:
                await admin.see_admin(message, message.from_user.id)
                await bot.send_message(message.from_user.id, messagetext['remove_admin'], reply_markup=keyboard.button_2, parse_mode=types.ParseMode.HTML)
                await admin.Remove_admin.message.set()
            elif message.text == buttonstext['see_admins']:
                await admin.see_admin(message, message.from_user.id)
            elif message.text == buttonstext['add_url']:
                await bot.send_message(message.from_user.id, messagetext['add_url'], reply_markup=keyboard.button_2, parse_mode=types.ParseMode.HTML)
                await url.Add_url.message.set()
            elif message.text == buttonstext['remove_url']:
                await url.see_url(message)
                await bot.send_message(message.from_user.id, messagetext['remove_url'], reply_markup=keyboard.button_2, parse_mode=types.ParseMode.HTML)
                await url.Remove_url.message.set()
            elif message.text == buttonstext['see_urls']:
                await url.see_url(message)


def registry_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(url_send, state=URL.message)
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_message_handler(menu, state = None)