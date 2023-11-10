from aiogram import Dispatcher, types
from create_bot import bot
from ..keyboard import main_kb
import database.dbsql


hello_text = ("""
🎃Уважаемые путешественники Зоны!🎃

Прошу извинения за 2дня отсутсвия, забыл оплатить хостинг а поднять серв не мог так как был не дома.
Так-же я исправил баг при котором не отображались арты с защитой от пси
Надеюсь вы провели отлично этот Хэллоуин

С наилучшими пожеланиями,
Разработчик StalAuction!
""")


# @dp.message_handler(commands=['update'])
async def send_message_update_all_users(message: types.Message):
    if message.from_user.id == 1254191582:
        data = database.dbsql.get_all_id_users()
        blocked_user = 0
        list_user = []
        for user in data:
            try:
                if user[0] not in list_user:
                    await bot.send_sticker(user[0],
                                           "CAACAgIAAxkBAAEKk1FlNKx8auj72PEN0OqPy1pH7uGKCAACQAEAAladvQps6VtALEnWJTAE")
                    await bot.send_message(user[0], hello_text, reply_markup=main_kb)
                    list_user.append(user[0])
                else:
                    pass
            except Exception:
                blocked_user += 1
        await message.answer(f"Пользователи получили сообщение, из них не получили {blocked_user}")


def register_admin_handler_update(dp: Dispatcher):
    dp.register_message_handler(send_message_update_all_users, commands=['update'])
