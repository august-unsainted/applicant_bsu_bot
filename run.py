import asyncio
from aiogram import Bot, Dispatcher

from handlers import start, olympiad, admission, scheme, calculator, dormitories, any_message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(start.router, olympiad.router, admission.router, scheme.router, calculator.router,
                       dormitories.router, any_message.router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
