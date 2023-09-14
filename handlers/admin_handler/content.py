from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from database.dbsql import get_all_id_users


class CreateRupor(StatesGroup):
    text = State()


@dp.message_handler(commands=['rupor'])
async def send_message_all_users(message: types.Message):
    if message.from_user.id == 1254191582:
        await message.answer('Введите текст')
        await CreateRupor.text.set()


@dp.message_handler(state=CreateRupor.text)
async def send_ticket_admin(message: types.Message, state: FSMContext):
    await state.finish()
    data = get_all_id_users()
    blocked_user = 0
    for user in data:
        try:
            await bot.send_message(user[0], message.text)
        except Exception:
            blocked_user += 1
    await message.answer(f"Пользователи получили сообщение, из них не получили {blocked_user}")
