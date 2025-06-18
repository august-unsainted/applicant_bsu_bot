from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN
from utils.data import keyboards, messages
from utils.db import count_users
from utils.send_broadcast import send_broadcast

router = Router()

cancel_kb, edit_kb, confirm_kb = [keyboards.get(f'{kb}_broadcast') for kb in ['cancel', 'edit', 'confirm']]


class Broadcast(StatesGroup):
    message_id = State()
    text = State()
    media = State()


async def handle_broadcast(context: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    args = {'text': messages.get("broadcast").format((await count_users()).get('active')), 'reply_markup': cancel_kb}
    response = await context.answer(**args) if isinstance(context, Message) else await context.message.edit_text(**args)
    await state.update_data(message_id=response.message_id)
    await state.set_state(Broadcast.text)


async def get_media(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], parse_mode='HTML',
                                reply_markup=edit_kb, text=messages.get('broadcast_text').format(message.text))
    await state.set_state(Broadcast.media)


async def get_result(state: FSMContext) -> str:
    data = await state.get_data()
    return messages.get('broadcast_result').format(data['text'], (await count_users()).get('active'))


@router.message(Command('mail'), F.chat.id == ADMIN)
async def cmd_mail(message: Message, state: FSMContext):
    await message.delete()
    await handle_broadcast(message, state)


@router.callback_query(F.data == 'broadcast')
async def broadcast(callback: CallbackQuery, state: FSMContext):
    await handle_broadcast(callback, state)


@router.callback_query(F.data == 'cancel_broadcast')
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.message(Broadcast.text)
async def get_broadcast_text(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await state.update_data(text=message.text)
    await get_media(message, state, bot)


@router.message(Broadcast.media)
async def get_broadcast_media(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    data = await state.get_data()
    message_id = data['message_id']
    if not message.photo:
        return await get_media(message, state, bot)
    media = message.photo[0].file_id
    await state.update_data(media=media)
    await bot.edit_message_media(chat_id=message.chat.id, message_id=message_id, reply_markup=confirm_kb,
                                 media=InputMediaPhoto(media=media, parse_mode='HTML', caption=await get_result(state)))


@router.callback_query(F.data == 'skip_pictures')
async def skip_pictures(callback: CallbackQuery, state: FSMContext):
    await state.update_data(media='')
    await callback.message.edit_text(await get_result(state), parse_mode='HTML', reply_markup=confirm_kb)


@router.callback_query(F.data == 'confirm_broadcast')
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()
    if data['media']:
        await callback.message.edit_caption(caption=f'⏳ <b>Рассылка в процессе…</b>', parse_mode='HTML')
    else:
        await callback.message.edit_text(f'⏳ <b>Рассылка в процессе…</b>', parse_mode='HTML')

    sender = callback.from_user
    admin_params = {'message_id': callback.message.message_id, 'chat_id': callback.message.chat.id}
    params = {key: data[key] for key in ['text', 'media']}

    await send_broadcast(bot, sender, admin_params, params)
