from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.olympiad import olympiad_kb, olympiad_back_kb

router = Router()


@router.callback_query(F.data == 'olympiad')
async def about_olympiad(callback: CallbackQuery):
    message_text = (
        '<b>Бесплатная олимпиада школьников «Байкальская перспектива» (7–11 классы)</b>\n\n'
        '<a href="https://my.bsu.ru/event/">Регистрация открыта!</a>\n\n'
        '<b>Олимпиада с 10-летней историей</b>, в которой приняли участие более 20 000 школьников из России и других стран. '
        'Включена в Перечень мероприятий Министерства просвещения РФ и перечень олимпиад на 2024/25 учебный год.\n\n'
        '<b>Цели олимпиады:</b>\n'
        '— Углубление интереса к общеобразовательным предметам.\n'
        '— Формирование навыков для поступления в профильные вузы.\n'
        '— Поиск и поддержка талантливых школьников.\n\n'
        '<b>Как принять участие?</b>\n'
        '1. <b>Регистрация</b>: до 10 декабря 2024 года <a href="https://my.bsu.ru/event/">на сайте олимпиады</a>.\n'
        '2. <b>Выбор профилей</b>: можно выбрать один или несколько из 12 направлений (см. ниже).\n'
        '3. <b>Этапы проведения</b>:\n'
        '— <u>Отборочный этап</u> (дистанционный): с 18 ноября по 10 декабря 2024 г.\n'
        '— <u>Заключительный этап</u> (очный): с 12 января по 2 февраля 2025 г.\n\n'
        '<b>Телеграм-канал олимпиады:</b>\n'
        '— @bp_bsu03\n\n'
        '<b>Подробнее по кнопкам ниже ↓</b>'
    )

    await callback.message.edit_text(message_text, parse_mode='HTML', reply_markup=olympiad_kb)


@router.callback_query(F.data.startswith('olympiad'))
async def get_info(callback: CallbackQuery):
    message_texts = {
        'rounds': (
            '<b>Этапы олимпиады</b>\n\n'
            '<b>Отборочный этап (дистанционный, online-тестирование):</b>\n'
            '— Даты проведения: с 18 ноя. по 10 дек. 2024 г.\n'
            '— Участники выполняют задания дома и загружают работы в личный кабинет.\n'
            '— Результаты: 20 дек.\n\n'
            '<b>Заключительный этап (очный):</b>\n'
            '— Даты проведения: с 12 янв. по 2 фев. 2025 г.\n'
            '— Место: региональные площадки.\n\n'
            '<b>Расписание заключительного этапа:</b>\n'
            '— 12 янв: математика, география, биология.\n'
            '— 19 янв: история, информатика, химия.\n'
            '— 26 янв: экономика, медицина, физика.\n'
            '— 2 фев: английский язык, литература, право.\n\n'
            '<b>Результаты заключительного этапа</b> (2025 г.):\n'
            '— Предварительные: 20 фев.\n'
            '— Апелляции: 21 фев.\n'
            '— Итоговые: 28 фев.'
        ),
        'profiles': (
            '<b>Профили олимпиады</b>\n\n'
            '<b>4-й уровень сложности:</b>\n'
            '— Математика, физика, информатика (7–11 классы)\n'
            '— Химия (8–11 классы)\n'
            '— Медицина, право, экономика (9–11 классы)\n\n'
            '<b>3-й уровень сложности:</b>\n'
            '— Биология, география, история, английский язык, литература (7–11 классы)'
        ),
        'privileges': (
            '<b>Привилегии для участников</b>\n\n'
            '<b>Доп. баллы к ЕГЭ (или ВВИ) <u>при поступлении в БГУ</u>:</b>\n'
            '— Победители/призёры <b>отборочного</b> этапа: <b>+3 балла</b>.\n'
            '— Победители/призёры <b>заключительного</b> этапа: <b>+10 баллов</b>.\n\n'
            'Доп. баллы в других вузах начисляются на усмотрение университета в соответствии с приказом № 1076 от 21 '
            'августа 2020 г.\n\n'
            '<b>Основание</b>:\n'
            '— Пункт 72, абзац 7 порядка приёма на обучение по образовательным программам высшего образования '
            '(постановление Минобрнауки РФ № 1076 от 21.08.2020).'
        ),
        'documents': (
            '<b>Документы об олимпиаде</b>\n\n'
            'https://www.bsu.ru/abit/olympics/bsu-olimp/17249/dokyment/'
        ),
        'organizers': (
            '<b>Соорганизаторы олимпиады</b>\n\n'
            '<b>Министерства Республики Бурятия:</b>\n'
            '— образования и науки,\n'
            '— природных ресурсов и экологии,\n'
            '— здравоохранения.\n\n'
            '<b>Научные организации СО РАН:</b>\n'
            '— Байкальский институт природопользования,\n'
            '— Институт биологии,\n'
            '— Институт физического материаловедения,\n'
            '— Институт монголоведения, буддологии и тибетологии.'
        ),
        'contacts': (
            '<b>Контакты организационного комитета</b>\n\n'
            '<b>Телефоны (добавочный 147):</b>\n'
            '— 8 (3012) 21-74-26\n'
            '— 8 (3012) 297-160\n'
            '— 8 (3012) 22-77-22\n\n'
            '<b>Адрес:</b>\n'
            '— г. Улан-Удэ, ул. Смолина, 24а, кабинет 0105\n\n'
            '<b>E-mail:</b>\n'
            '— olympic@bsu.ru'
        )
    }

    info_type = callback.data.replace('olympiad_', '')
    await callback.message.edit_text(message_texts[info_type], parse_mode='HTML', reply_markup=olympiad_back_kb)
