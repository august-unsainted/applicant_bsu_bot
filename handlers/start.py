from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.start import start_kb, start_back_kb

router = Router()

message_text = (
    'Здравствуйте!\n\n'
    'Вы обратились к боту-помощнику для абитуриентов Бурятского государственного '
    'университета им. Д. Банзарова.\n\n'
    'Выберите интересующую Вас категорию вопроса.'
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(message_text, parse_mode='HTML', reply_markup=start_kb)


@router.callback_query(F.data == 'start')
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(message_text, parse_mode='HTML', reply_markup=start_kb)


@router.callback_query(F.data.in_({'exams', 'links', 'developers'}))
async def exams(callback: CallbackQuery):
    message_texts = {
        'exams': (
            '<b>Образовательная акция «Пробный ЕГЭ»</b>\n\n'
            'Уважаемые старшеклассники! Приглашаем вас проверить свои знания на пробных ЕГЭ. '
            '<a href="https://www.bsu.ru/reg/?reg_form=1">Зарегистрироваться</a>\n\n'
            '<b>Актуальная информация ЕГЭ 2024:</b>\n'
            '— https://vk.com/priem_bsu\n\n'
            '<b>Стоимость:</b>\n'
            '— 200 рублей за один предмет\n\n'
            '<b>Расписание на 2023 г:</b>\n'
            '— 20 января в 14:00: Химия, информатика и ИКТ\n'
            '— 28 января в 10:00: Математика (профильный уровень)\n'
            '— 3 февраля в 14:00: Биология, физика\n'
            '— 10 февраля в 14:00: Обществознание\n\n'
            '<b>Результаты:</b>\n'
            '— Через 10 дней на информационном стенде в каб. 0105\n\n'
            '<b>Место проведения:</b>\n'
            '— г. Улан-Удэ, ул. Смолина, 24а\n'
            '<b>Контактный телефон:</b>\n'
            '— +7 (3012) 22-77-22'),
        'links': (
            '<b>Полезные ссылки:</b>\n'
            '— <a href="https://t.me/priem_bsu_bot">Телеграм-бот для вопросов</a>\n'
            '— <a href="https://vk.com/priem_bsu">Приемная комиссия БГУ в ВК</a>\n'
            '— <a href="https://vk.com/bsu03">Официальная группа БГУ в ВК</a>.\n\n'
            '<b>Прочее:</b>\n'
            '— <a href="https://abiturient.bsu.ru/test/">Тест профессиональной направленности</a>\n'
            '— <a href="https://www.bsu.ru/abit/qa/">Часто задаваемые вопросы</a>\n'
            '— <a href="https://www.bsu.ru/abit/help/profession/">Словарь профессий</a>'),
        'developers': (
            '<b>О разработчиках бота-помощника</b>\n\n'
            'Этот бот был создан в рамках конкурса грантов на инициативные научные исследования Бурятского государственного университета (БГУ).\n\n'
            '<b>Разработчиками являются студенты колледжа БГУ:</b>\n'
            '— <a href="https://t.me/mrkos34">Иванов Роман</a>\n'
            '— <a href="https://t.me/mhidt">Доржеева Виктория</a>.\n\n'
            'Если вы заинтересованы в сотрудничестве, напишите нам в личные сообщения.'
        )
    }

    await callback.message.edit_text(message_texts[callback.data], parse_mode='HTML', reply_markup=start_back_kb,
                                     disable_web_page_preview=True)


# @router.callback_query(F.data == 'links')
# async def links(callback: CallbackQuery):
#     await callback.message.edit_text(
#         '<b>Полезные ссылки:</b>\n'
#         '— <a href="https://t.me/priem_bsu_bot">Телеграм-бот для вопросов</a>\n'
#         '— <a href="https://vk.com/priem_bsu">Приемная комиссия БГУ в ВК</a>\n'
#         '— <a href="https://vk.com/bsu03">Официальная группа БГУ в ВК</a>.\n\n'
#         '<b>Прочее:</b>\n'
#         '— <a href="https://abiturient.bsu.ru/test/">Тест профессиональной направленности</a>\n'
#         '— <a href="https://www.bsu.ru/abit/qa/">Часто задаваемые вопросы</a>\n'
#         '— <a href="https://www.bsu.ru/abit/help/profession/">Словарь профессий</a>',
#         parse_mode='HTML', reply_markup=start_back_kb, disable_web_page_preview=True)
#
#
# @router.callback_query(F.data == 'developers')
# async def developers(callback: CallbackQuery):
#     await callback.message.edit_text(
#         '<b>О разработчиках бота-помощника</b>\n\n'
#         'Этот бот был создан в рамках конкурса грантов на инициативные научные исследования Бурятского государственного университета (БГУ).\n\n'
#         '<b>Разработчиками являются студенты колледжа БГУ:</b>\n'
#         '— <a href="https://t.me/mrkos34">Иванов Роман</a>\n'
#         '— <a href="https://t.me/mhidt">Доржеева Виктория</a>.\n\n'
#         'Если вы заинтересованы в сотрудничестве, напишите нам в личные сообщения.',
#         parse_mode='HTML', reply_markup=start_back_kb, disable_web_page_preview=True)
