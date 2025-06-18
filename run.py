import asyncio
import sys
from aiogram import Bot, Dispatcher
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from handlers import start, calculator, broadcast, statistics
from config import TOKEN
from utils.app import MainWindow
from utils.db import start_db

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def run_bot():
    await start_db()
    dp.include_routers(calculator.router, broadcast.router, statistics.router, start.router)
    await dp.start_polling(bot, skip_updates=True)


async def main():
    bot_task = asyncio.create_task(run_bot())
    window = MainWindow(bot_task)
    window.show()

    try:
        await bot_task
    except asyncio.CancelledError:
        print("Бот остановлен по команде GUI")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, RuntimeError):
        print('Бот остановлен вручную')
