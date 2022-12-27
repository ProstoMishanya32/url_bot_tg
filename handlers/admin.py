import aiogram
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randrange
from create_bot import dp, bot
from configs.text import messagetext, errortext, buttonstext
from modules import json_logic, keyboard

class Add_admin(StatesGroup):
	message = State()

async def add_admin(message: types.Message, state: FSMContext):
	try:
		if message.text == buttonstext['cancel']:
			await state.finish()
			await bot.send_message(message.from_user.id, messagetext['start'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
		else:
			user_id = message['forward_from']['id']
			if message['forward_from']['last_name'] == None:
				nickname = message['forward_from']['first_name']
			else:
				nickname = f"{message['forward_from']['first_name']} {message['forward_from']['last_name']}"
			await json_logic.add_admin(user_id, nickname)
			await bot.send_message(message.from_user.id, messagetext['successfully'],  reply_markup = keyboard.button_1)
			await state.finish()
	except TypeError:
		await bot.send_message(message.from_user.id, errortext['error_forward_message'], parse_mode=types.ParseMode.HTML)

class Remove_admin(StatesGroup):
	message = State()

async def remove_admin(message: types.Message, state: FSMContext):
	if message.text == buttonstext['cancel']:
		await state.finish()
		await bot.send_message(message.from_user.id, messagetext['start'], reply_markup = keyboard.button_1, parse_mode=types.ParseMode.HTML)
	else:
		remove = await json_logic.remove_admin(message.text)
		if remove == True:
			await state.finish()
			await bot.send_message(message.from_user.id, messagetext['successfully'], reply_markup = keyboard.button_1)
		else:
			await state.finish()
			await bot.send_message(message.from_user.id, errortext['user_not_finden'], reply_markup = keyboard.button_1)

async def see_admin(message, user_id):
	admins = await json_logic.get_admins()
	if message.chat.type == "private":
		if message.from_user.id in admins:
			admins = await json_logic.see_admins()
			message = ''
			if admins:
				for character in admins:
					message += f"<b> #{character['position']}  {character['nickname']} || {character['user_id']}</b>\n"
				await bot.send_message(user_id, message, reply_markup = keyboard.button_1,  parse_mode=types.ParseMode.HTML)



def registry_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(add_admin, state = Add_admin.message )
	dp.register_message_handler(remove_admin, state = Remove_admin.message )