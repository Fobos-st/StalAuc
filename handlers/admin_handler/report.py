from aiogram import types, Dispatcher

from database.dbsql import get_count_user


# @dp.message_handler(commands=['statistics'])
async def send_count_user_in_db(message: types.Message):
    if message.from_user.id == 1254191582:
        await message.answer(get_count_user())


def register_admin_handler_report(dp: Dispatcher):
    dp.register_message_handler(send_count_user_in_db, commands=['statistics'])
