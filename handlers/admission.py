from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.admission import admission_kb, admission_back_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    message_text = (
        '<b>Приемная кампания в БГУ</b> (2024 г.)\n'
        '1340 бюджетных мест\n\n'
        '<b>Телеграм-бот для вопросов:</b>\n'
        '— @priem_bsu_bot\n\n'
        '— <a href="https://vk.com/priem_bsu">Приемная комиссия БГУ в ВК</a>\n\n'
        '— <a href="https://www.bsu.ru/pk/">Больше информации на официальном сайте</a>.'
    )

    await message.answer(message_text, parse_mode='HTML', reply_markup=admission_kb)


@router.callback_query(F.data.startswith('admission'))
async def get_info(callback: CallbackQuery):
    message_texts = {
        'start': (
            '<b>Приемная кампания в БГУ</b> (2024 г.)\n'
            '1340 бюджетных мест\n\n'
            '<b>Телеграм-бот для вопросов:</b>\n'
            '— @priem_bsu_bot\n\n'
            '— <a href="https://vk.com/priem_bsu">Приемная комиссия БГУ в ВК</a>\n\n'
            '— <a href="https://www.bsu.ru/pk/">Больше информации на официальном сайте</a>.'
        ),
        'forms_and_requirements': (
            'Формы обучения и требования:\n\n'
            'Колледж (2-4 года): аттестат (9/11 классов).\n'
            '・  <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            'Бакалавриат (4 года): баллы ЕГЭ или диплом СПО и внутренние экзамены.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            'Специалитет (5-6 лет): баллы ЕГЭ или диплом СПО и внутренние экзамены.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            'Магистратура (2 года): диплом о высшем образовании и внутренний экзамен.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            'Аспирантура (3-4 года): диплом специалиста/магистра и внутренний экзамен.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>\n\n'
            'Ординатура (2 года): медицинский диплом и федеральное тестирование.\n'
            '・ <a href="https://www.bsu.ru/abit/camp2024/spo2024/">Читать подробнее</a>'
        ),
        'documents': (
            '<b>Приём документов БГУ:</b>\n\n'
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
            '— +7 (3012) 22-77-22'
        ),
        'links': (
            'Полезные ссылки:\n\n'
            '— <a href="https://vk.com/bsu03">Официальная группа БГУ в ВК</a>\n\n'
            '— <a href="https://abiturient.bsu.ru/test/">Тест профессиональной направленности</a>\n\n'
            '— <a href="https://www.bsu.ru/abit/qa/">Часто задаваемые вопросы</a>\n\n'
            '— <a href="https://www.bsu.ru/abit/help/profession/">Словарь профессий</a>'
        )
    }

    info_type = callback.data.replace('admission_', '')
    markup = admission_kb if info_type == 'start' else admission_back_kb
    await callback.message.edit_text(message_texts[info_type], parse_mode='HTML', reply_markup=markup)




