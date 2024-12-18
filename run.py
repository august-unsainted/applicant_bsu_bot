import asyncio
from aiogram import Bot, Dispatcher

from handlers import olympiad, admission, scheme, calculator
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(olympiad.router, admission.router, scheme.router, calculator.router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
