import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randrange
from create_bot import dp, bot
from configs.text import messagetext, errortext, buttonstext
from modules import json_logic, keyboard, sqlite_logic

class Add_url(StatesGroup):
	message = State()

async def add_url(message: types.Message, state: FSMContext):
	try:
		if message.text == buttonstext['cancel']:
			await state.finish()
			await bot.send_message(message.from_user.id, messagetext['start'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
		else:
			result, check = await sqlite_logic.create_url(message.text)
			if check == True:
				await bot.send_message(message.from_user.id, messagetext['url_code'].format(code = result), reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
				await state.finish()
			else:
				await bot.send_message(message.from_user.id, errortext['url_code'].format(code = result), reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
				await Add_url.message.set()
	except:
		await bot.send_message(message.from_user.id, errortext['error'], parse_mode=types.ParseMode.HTML)

class Remove_url(StatesGroup):
	message = State()

async def remove_url(message: types.Message, state: FSMContext):
	try:
		if message.text == buttonstext['cancel']:
			await state.finish()
			await bot.send_message(message.from_user.id, messagetext['start'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
		else:
			check = await sqlite_logic.remove_url(message.text)
			if check == True:
				await bot.send_message(message.from_user.id, messagetext['url_remove_code'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
				await state.finish()
			else:
				await bot.send_message(message.from_user.id, errortext['url_remove_code'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
				await Remove_url.message.set()
	except:
		await bot.send_message(message.from_user.id, errortext['error'], parse_mode=types.ParseMode.HTML)

async def see_url(message):
	urls = await sqlite_logic.get_Url()
	if len(urls) == 0:
		await bot.send_message(message.from_user.id, messagetext['len_url'], reply_markup=keyboard.button_1, parse_mode=types.ParseMode.HTML)
	else:
		text = []
		for i in urls:
			text.append(f"{i[0]} - {i[1]}")
		temp = '\n'
		await bot.send_message(message.from_user.id, f"<b>КОД - ССЫЛКА</b>\n{temp.join(text)}", reply_markup=keyboard.button_1, parse_mode=types.ParseMode.HTML)

def registry_handlers_url(dp: Dispatcher):
	dp.register_message_handler(add_url, state = Add_url.message )
	dp.register_message_handler(remove_url, state = Remove_url.message )
