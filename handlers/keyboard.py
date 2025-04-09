from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_continue = [[InlineKeyboardButton(text="Далее", callback_data="continue_button")]]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=button_continue)
