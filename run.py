import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, calculator, broadcast, statistics
from config import TOKEN
from utils.db import start_db

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await start_db()
    dp.include_routers(calculator.router, broadcast.router, statistics.router, start.router)
    print('Бот включен')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print('Бот остановлен вручную')
