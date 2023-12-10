import sqlite3


db = sqlite3.connect('serv.db')
cursor = db.cursor()


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
        cursor.execute(f"SELECT * FROM users WHERE user_id = '{1254191582}'")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (1254191582, "wg53", 12, '1', 12))
            db.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)


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
        cursor.execute("SELECT * FROM users GROUP BY user_id")
        return f"Количество пользователей: {len(cursor.fetchall())}"
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite \n",
              error)
