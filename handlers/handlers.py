__all__ = [
    "router",
]

from aiogram.filters import Command
from aiogram import Router

router = Router()

@router.message(Command("help"))
async def process_start_command(message):
    await message.answer("ПОМОГИ!")

@router.message(Command(commands=["start", "status"]))
async def process_start_command(message):
    await message.reply(f"{message.from_user.id}, {message.from_user.username}")