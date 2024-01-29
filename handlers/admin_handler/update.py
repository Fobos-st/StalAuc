from aiogram import Dispatcher, types
from create_bot import bot
from ..keyboard import main_kb
import database.dbsql
# ❄️Уважаемые путешественники Зоны!❄️

hello_text = ("""
🎉🥳Нас 1тыс!🥳🎉

На 144день жизни проекта мы преодолели значительное число пользователей, теперь нас более 1тыс!!!

Я невероятно благодарен каждому для кого бот стал удобным инструментом котором вы пользуетесь с удовольствием, каждому кто доверился мне и не побоялся узнать что это за бот!

Поверьте дальше больше!

С уважением,
🎉разработчик StalAuction!🥳
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
