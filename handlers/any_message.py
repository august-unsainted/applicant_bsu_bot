from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def any_message(message: Message):
    await message.answer('К сожалению, я не понимаю, что вы хотите сказать 😢')
    await message.delete()
