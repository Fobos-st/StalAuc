from aiogram import Dispatcher, types
from create_bot import bot
from ..keyboard import main_kb
import database.dbsql
# ❄️Уважаемые путешественники Зоны!❄️

hello_text = ("""
❄️Уважаемые путешественники Зоны!❄️

Новое обновление с оптимизацией имеющихся проблем и нововведениями

1)Количество предметов используемых в расчёте средней цены  
2)Оптимизация 'средней цены'
3)Оптимизация 'ожидания предмета' 

Подробнее об обновление можно прочитать тут - https://telegra.ph/Patchnout-27012024-01-27

Спасибо за внимание!

С уважением,
разработчик StalAuction!
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
