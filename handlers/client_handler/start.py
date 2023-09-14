from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..keyboard import main_kb
from database.dbsql import reg
from create_bot import bot


# @dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("""Бот находится в разработке и на данный момент он в MVP состояние
Проще говоря в бета-тесте""")
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton('Русский', callback_data='Russian'))
    await message.answer('Привет! Выберите язык', reply_markup=ikb)


# @dp.callback_query_handler(text=['Russian'])
async def cmd_server_selection(callback_query: types.CallbackQuery):
    # language depending on the choice
    reg(callback_query.from_user.id)
    ikb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    ikb.add(InlineKeyboardButton('RU', callback_data='RU'))
    await bot.send_message(callback_query.from_user.id, "Выберети ваш игровой сервер:", reply_markup=ikb)


# @dp.callback_query_handler(text=['RU'])
async def cmd_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, """
В данном боте есть 2 функции
1)Самая обычная проверка цен на аукционе
2)Ожидание предмета на аукционе с определённой ценной и качеством в случае с артефактом
(Получается при появление нужного предмета, с нужной, вам отправится сообщение об этом)
(Может работать не стабильно)
Удачи сталкер
""", reply_markup=main_kb)


def register_client_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(cmd_server_selection, text=['Russian'])
    dp.register_callback_query_handler(cmd_main, text=['RU'])
