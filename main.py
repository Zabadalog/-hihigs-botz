# version: 0.1.0
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router, set_my_commands, set_up_logger

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)

    # Запуск логирования
    set_up_logger(fname=__name__)

    await set_my_commands(bot)

    # Запуск бота в polling-режим
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())