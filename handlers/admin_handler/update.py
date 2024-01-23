from aiogram import Dispatcher, types
from create_bot import bot
from ..keyboard import main_kb
import database.dbsql
# ❄️Уважаемые путешественники Зоны!❄️

hello_text = ("""
❄️Уважаемые путешественники Зоны!❄️

Я вернулся домой и приступил к разработке обратно!
Так что готов вновь вас радовать обновлениями.

Обновление:

1)В функцию "проверка цены" на предметы, чьё количество больше 1, добавлена информация об их количестве и цена за 1шт.
2)Исправил ошибку при которой могла не работать средняя цена на предметы 
3)Возможность подержать данный проект монетой, вся сумма будет уходить строго на оплату хостинга!
4)Обновлена база данных новыми предметами

Спасибо что остаётесь со мной,
С уважением разработчик StalAuction!
""")


# @dp.message_handler(commands=['update'])
async def send_message_update_all_users(message: types.Message):
    if message.from_user.id == 1254191582:
        data = database.dbsql.get_all_id_users()
        blocked_user = 0
        for user in data:
            try:
                await bot.send_message(user[0], hello_text, reply_markup=main_kb)
            except Exception:
                blocked_user += 1
        await message.answer(f"Пользователи получили сообщение, из них не получили {blocked_user}")


def register_admin_handler_update(dp: Dispatcher):
    dp.register_message_handler(send_message_update_all_users, commands=['update'])
