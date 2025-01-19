from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.admission import admission_kb, admission_back_kb

router = Router()


@router.callback_query(F.data == 'admission')
async def admission(callback: CallbackQuery):
    message_text = (
        '<b>Приемная кампания в БГУ</b> на 2024 год: 1340 бюджетных мест\n\n'
        ' ・ ПРИЕМ ДОКУМЕНТОВ на все формы обучения с 20 июня 2024 г.\n\n'
        '— <a href="https://www.bsu.ru/pk/">Подробнее о приёмной компании</a>\n'
        '— <a href="https://vk.com/priem_bsu">Приемная комиссия БГУ в ВК</a>\n'
        '— <a href="https://t.me/priem_bsu_bot">Телеграм-бот для вопросов</a>'
    )
    await callback.message.edit_text(message_text, parse_mode='HTML', reply_markup=admission_kb,
                                     disable_web_page_preview=True)


@router.callback_query(F.data.in_({'contacts', 'forms'}))
async def get_info(callback: CallbackQuery):
    message_texts = {
        'contacts': (
            '<b>Расписание приёма документов в БГУ и контакты:</b>\n\n'
            '<b>Начало приема на все формы:</b>\n'
            '— с 20 июня 2024 года\n\n'
            '<b>Расписание:</b>\n'
            '— С Пн по Пт: с 9:00 до 17:00\n'
            '— СБ и ВС: выходные\n\n'
            '<b>Почтовый адрес:</b>\n'
            '— 670000, г. Улан-Удэ, ул. Смолина, 24 а, Приемная комиссия БГУ, каб. 0105\n\n'
            '<b>Телефоны:</b>\n'
            '— 8 (3012) 22-77-22 (многоканальный)\n'
            '— 8 (3012) 21-74-26\n\n'
            '<b>E-mail:</b>\n'
            '— udp@bsu.ru'
        ),
        'forms': (
            '<b>Формы обучения и требования:</b>\n\n'
            '<b>Колледж (2-4 года):</b> аттестат (9/11 классов).\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            '<b>Бакалавриат (4 года):</b> баллы ЕГЭ или диплом СПО и внутренние экзамены.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/bak2024/">Читать подробнее</a>\n\n'
            '<b>Специалитет (5-6 лет):</b> баллы ЕГЭ или диплом СПО и внутренние экзамены.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spec2024/">Читать подробнее</a>\n\n'
            '<b>Магистратура (2 года):</b> диплом о высшем образовании и внутренний экзамен.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/mag2024/">Читать подробнее</a>\n\n'
            '<b>Аспирантура (3-4 года):</b> диплом специалиста/магистра и внутренний экзамен.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/asp2024/">Читать подробнее</a>\n\n'
            '<b>Ординатура (2 года):</b> медицинский диплом и федеральное тестирование.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/ord2024/">Читать подробнее</a>'
        ),
    }

    await callback.message.edit_text(message_texts[callback.data], parse_mode='HTML', reply_markup=admission_back_kb)




