from aiogram import types
from create_bot import dp
from DataBase.sqlite import get_count_user


@dp.message_handler(commands=['statistics'])
async def send_count_user_in_db(message: types.Message):
    if message.from_user.id == 1254191582:
        await message.answer(get_count_user())
