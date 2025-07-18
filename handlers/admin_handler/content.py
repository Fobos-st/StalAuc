from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot
from ..keyboard import main_kb
from database.dbsql import get_all_id_users


class CreateRupor(StatesGroup):
    text = State()


class CreateRequestUser(StatesGroup):
    text = State()
    id_user = State()


# @dp.message_handler(commands=['rupor'])
async def send_message_all_users(message: types.Message):
    if message.from_user.id == 1254191582:
        await message.answer('Введите текст')
        await CreateRupor.text.set()


# @dp.message_handler(state=CreateRupor.text)
async def send_message(message: types.Message, state: FSMContext):
    await state.finish()
    data = get_all_id_users()
    blocked_user = 0
    for user in data:
        try:
            await bot.send_message(user[0], message.text, reply_markup=main_kb)
        except Exception:
            blocked_user += 1
    await message.answer(f"Пользователи получили сообщение, из них не получили {blocked_user}")


#  @dp.message_handler(commands=['answer'])
async def send_answer_user(message: types.Message):
    if message.from_user.id == 1254191582:
        await CreateRequestUser.text.set()
        await message.answer("Текст")


# @dp.message_handler(state=CreateRequestUser.text)
async def get_answer_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await CreateRequestUser.next()
    await message.answer("id")


# @dp.message_handler(state=CreateRequestUser.id_user)
async def get_answer_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.send_message(int(message.text), f"Ответ от разаботчика \n{data['text']}", reply_markup=main_kb)
        await message.answer("Пользователь получил ответ")
        await state.finish()
    except Exception:
        await message.answer("Пользователь не получил ответ")
        await state.finish()


def register_admin_handler_content(dp: Dispatcher):
    dp.register_message_handler(send_message_all_users, commands=['rupor'])
    dp.register_message_handler(send_message, state=CreateRupor.text)
    dp.register_message_handler(send_answer_user, commands=['answer'])
    dp.register_message_handler(get_answer_text, state=CreateRequestUser.text)
    dp.register_message_handler(get_answer_id, state=CreateRequestUser.id_user)
