from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from configs.text import buttonstext
button_1 = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(KeyboardButton(
	buttonstext['add_url'])).insert(KeyboardButton(
	buttonstext['remove_url'])).add(KeyboardButton(
	buttonstext['see_urls'])).insert(KeyboardButton(
	buttonstext['add_admin'])).add(KeyboardButton(
	buttonstext['remove_admin'])).insert(KeyboardButton(
	buttonstext['see_admins']))

button_2 =  ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(KeyboardButton(buttonstext['cancel']))