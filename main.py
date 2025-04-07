import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
from handlers import set_up_logger

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)

    # Запуск логирования
    set_up_logger(fname=__name__)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
