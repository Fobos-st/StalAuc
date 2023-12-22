import sqlite3

db = sqlite3.connect('serv.db')
cursor = db.cursor()


reg_in_raffle = """
Привет! Теперь ты принимаешь участие в розыгрыше на БП. 
Условия участия просты!
1)Не блокировать бота до 30 числа, что-бы можно было получить уведомление о выигрыше, и всё!
Количество участников - {}
Ваш шанс - {}
"""

reg_in_raffle1 = """
И вновь привет!
Надеюсь ты не хотел нагнуть систему
и принять участие вновь)
Твои текущие шансы на победу:
Количество участников - {}
Ваш шанс - {}
"""


def create_table() -> None:
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT,
            item_id TEXT,
            price INT,
            quality TEXT,
            additional TEXT
        )""")
        db.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS new_years_gift (
            user_id INT,
            user_name TEXT
        )""")
        db.commit()

        cursor.execute(f"SELECT * FROM users WHERE user_id = '{1254191582}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (1254191582, "wg53", 12, '1', 12))
            db.commit()

        cursor.execute("SELECT * FROM new_years_gift WHERE user_id = '1254191582'")
        if cursor.fetchone() is None:
            for i in range(5):
                cursor.execute(f"INSERT INTO new_years_gift (user_id, user_name) VALUES (1254191582, 'Чыхпых(Иронично что я разработчик самого бота)')")
            db.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


async def reg_in_sweepstakes(user_id: int, user_name: str) -> str:
    db = sqlite3.connect('serv.db')
    try:
        cursor.execute(f"SELECT * FROM new_years_gift WHERE user_id = '{user_id}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO new_years_gift (user_id, user_name) VALUES ({user_id}, '{user_name}')")
            db.commit()
            return reg_in_raffle.format(await get_count_user_raffle(), f"{round((1 / await get_count_user_raffle()) * 100, 2)}%")
        else:
            return reg_in_raffle1.format(await get_count_user_raffle(), f"{round((1 / await get_count_user_raffle()) * 100, 2)}%")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


async def get_count_user_raffle() -> int:
    cursor.execute("SELECT COUNT(user_id) FROM new_years_gift")
    result = cursor.fetchall()
    return result[0][0] - 4


async def print_all_users():
    cursor.execute('SELECT * FROM users GROUP BY user_id')
    users = cursor.fetchall()
    return users


def get_all_id_users():
    cursor.execute("SELECT user_id FROM users GROUP BY user_id")
    result = cursor.fetchall()
    return result


def reg(user_id: int) -> None:
    db = sqlite3.connect('serv.db')
    try:
        cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        print(cursor.fetchone())
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, 'None', 'None', 'None', 'None'))
            db.commit()
        else:
            pass
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


def update_sqlite_table(user_id, item, price, quality=None, additional="All"):
    try:
        sql_update = f"""UPDATE users SET item_id = '{item}', price = '{price}', quality = '{quality}', additional = '{additional}' WHERE user_id = '{user_id}'"""
        cursor.execute(sql_update)
        db.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


def get_request_user(user_id: int):
    try:
        for i in cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'"):
            return i
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


def delete_request(user_id):
    try:
        sql_update = f"""UPDATE users SET item_id = 'None', price = 'None', quality = 'None', additional = 'None' WHERE user_id = '{user_id}'"""
        cursor.execute(sql_update)
        db.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


def get_count_user():
    try:
        cursor.execute("SELECT COUNT(user_id) FROM users GROUP BY user_id")
        return f"Количество пользователей: {len(cursor.fetchall())}"
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)
