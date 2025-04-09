import logging
from aiogram.filters import Command
from aiogram import Router, F
from .keyboard import main_keyboard

router = Router()

@router.message(Command("help"))
async def process_start_command(message):
    await message.answer("ПОМОГИ!")
    logging.info(f"User with id={message.from_user.id} need help")

@router.message(Command(commands=["start", "status"]))
async def process_start_command(message):
    await message.reply(f"ID{message.from_user.id}, User: {message.from_user.username}", reply_markup=main_keyboard)
    logging.info(f"User with id={message.from_user.id} launched the bot")

@router.message()
async def echo_message(message):
    await message.answer(message.text)
    logging.info(f"User with id={message.from_user.id} sent an unprocessable message")

@router.callback_query(F.data.startswith("continue"))
async def callback_continue(callback):
    await callback.message.answer(text="Успешно вызван callback!")
