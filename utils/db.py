import sqlite3 as sq
import pytz
from typing import Any
from datetime import datetime

from utils.data import stats, keyboards_text, messages_text
from utils.filesystem import find_resource_path

db = sq.connect(find_resource_path('data/applicant.db'))
cur = db.cursor()

months_dict = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}

tz = pytz.timezone('Asia/Irkutsk')


def get_stat_name(stat: str) -> str | None:
    for key, value in keyboards_text.items():
        for callback, text in value.items():
            if callback == stat:
                return text


def get_table_name() -> str:
    now = datetime.now(tz=tz)
    month, year = now.month, now.year
    return f'stats_{month}_{year}'


async def start_db():
    stats_table = get_table_name()
    cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {stats_table} (
                button text PRIMARY KEY,
                count INTEGER DEFAULT 0
                )
            ''')
    cur.executemany(f'''
        INSERT OR IGNORE INTO {stats_table} (button)
        VALUES (?)
    ''', [(btn,) for btn in stats + ['active_users', 'inactive_users']])
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                is_active INTEGER DEFAULT 1
                )
            ''')
    db.commit()


async def execute_query(query: str, *args: Any) -> None | list[tuple]:
    result = cur.execute(query, tuple(args))
    db.commit()
    if query.strip().startswith('SELECT'):
        return result.fetchall()


async def add_user(user_id: int | str) -> None:
    await execute_query(
        '''
            INSERT INTO users (user_id)
            VALUES (?)
            ON CONFLICT(user_id)
            DO UPDATE SET is_active = 1;
        ''',
        str(user_id))


async def count_users() -> dict[str, int]:
    result = {}
    table = get_table_name()
    for is_active in [1, 0]:
        key = f"{'in' * (not is_active)}active"
        result[key] = len(await execute_query('SELECT * FROM users WHERE is_active = ?', is_active))
        await execute_query(f"UPDATE {table} SET count = ? WHERE button = ?", result[key], key + '_users')

    result['all'] = sum(result.values())
    return result


async def get_active_users() -> list[int]:
    results = await execute_query('SELECT user_id FROM users WHERE is_active = 1')
    return [result[0] for result in results]


async def update_activity(user_id: int | str, activity: bool = False) -> None:
    await execute_query('UPDATE users SET is_active = ? WHERE user_id = ?;', activity, str(user_id))


async def increase_stat_count(button: str) -> None:
    await execute_query(
        f'''
            UPDATE {get_table_name()}
            SET count = count + 1
            WHERE button = ?
        ''',
        button
    )


async def get_stat_dict(table: str) -> dict[str, int]:
    table = table or get_table_name()
    entries = await execute_query(f'SELECT * FROM {table}')
    result = {}
    for entry in entries:
        btn = entry[0]
        result[get_stat_name(btn) or btn] = entry[1]
    return result


async def get_stat(table: str = '', temp: dict[str, int] = None) -> tuple[int, Any, int | Any, str]:
    if temp is None:
        temp = {}
    table = await get_stat_dict(table)
    result, total, users = [], 0, []
    for text, count in table.items():
        if not text.endswith('users'):
            result.append(f'— «{text}»: {count}')
            total += count
        else:
            count -= temp.get(text) or 0
            users.append(count)
    return sum(users), *users, total, '\n'.join(result)


async def get_stats() -> list[str]:
    template = messages_text.get('stat')
    main_text = messages_text.get('all_stat').format(*await get_stat())
    months = []
    temp = {}
    tables = await execute_query('SELECT name FROM sqlite_master WHERE type="table"')
    for table in tables:
        table = table[0]
        if not table.startswith('stats'):
            continue
        month_number, year = table.replace('stats_', '').split('_')
        month = months_dict.get(int(month_number))
        header = f'{month}, {year}'
        record_stat = template.format(*await get_stat(table, temp))
        months.append(f'<b>{header}\n</b>\n{record_stat}')
        temp = await get_stat_dict(table)
    return [f'{main_text}\n\n<blockquote>🗓 {month}</blockquote>' for month in months][::-1]
