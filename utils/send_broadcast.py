import asyncio
from aiogram.exceptions import TelegramRetryAfter, TelegramAPIError, AiogramError, TelegramBadRequest
from aiogram import Bot
from aiogram.types import User

from utils.data import messages_text, keyboards
from utils.db import get_active_users, update_activity, count_users


async def send_message(user_id: str, func: callable, params: dict[str, str]) -> bool:
    try:
        await func(chat_id=user_id, **params)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_message(user_id, func, params)
    except (TelegramAPIError, AiogramError) as e:
        print(f"Ошибка отправки пользователю {user_id}: {e}")
        await update_activity(user_id)
    else:
        return True
    return False


async def send_broadcast(bot: Bot, sender: User, admin_params: dict, broadcast_params: dict) -> None:
    count = 0
    try:
        semaphore = asyncio.Semaphore(20)

        async def send(user_id):
            async with semaphore:
                message_text, media = broadcast_params['text'], broadcast_params['media']
                params = {'parse_mode': 'HTML', 'reply_markup': keyboards.get('broadcast')}
                if media:
                    func = bot.send_photo
                    params['photo'], params['caption'] = media, message_text
                else:
                    func = bot.send_message
                    params['text'] = message_text
                return await send_message(user_id, func, params)

        tasks = [asyncio.create_task(send(user_id)) for user_id in await get_active_users()]
        results = await asyncio.gather(*tasks)
        count = sum(1 for success in results if success)
        await count_users()
    finally:
        text = messages_text.get('broadcast_end').format(broadcast_params['text'], count, sender.first_name, sender.username)
        try:
            if broadcast_params['media']:
                await bot.edit_message_caption(caption=text, parse_mode='HTML', **admin_params)
            else:
                await bot.edit_message_text(text=text, parse_mode='HTML', **admin_params)
        except TelegramBadRequest:
            await bot.send_message(text=text, parse_mode='HTML', **admin_params)
