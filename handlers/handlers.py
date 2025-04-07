import logging
from aiogram.filters import Command
from aiogram import Router

# Установка логирования по умолчанию
logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(Command("help"))
async def process_start_command(message):
    await message.answer("ПОМОГИ!")
    logging.info(f"User with id={message.from_user.id} need help")

@router.message(Command(commands=["start", "status"]))
async def process_start_command(message):
    await message.reply(f"ID{message.from_user.id}, User: {message.from_user.username}")
    logging.info(f"User with id={message.from_user.id} launched the bot")

@router.message()
async def echo_message(message):
    await message.answer(message.text)
    logging.info(f"User with id={message.from_user.id} sent an unprocessable message")
