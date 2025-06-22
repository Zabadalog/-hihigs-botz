"""Entry point for running bot via the business logic package."""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers import all_routers, set_my_commands, set_up_logger
from .db import create_table
from .classes import YandexBotLogic

async def main() -> None:
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(*all_routers)

    set_up_logger(fname=__name__)
    await create_table()
    await set_my_commands(bot)

    logic = YandexBotLogic()
    print(logic)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
