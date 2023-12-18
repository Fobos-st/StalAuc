from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import text
from create_bot import bot
from database.dbsql import reg
from ..keyboard import main_kb


async def cmd_start(message: types.Message):  # cmd = start
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton('Русский', callback_data='Russian'))

    await bot.send_sticker(message.from_user.id, r"CAACAgIAAxkBAAEK0RllYhhasr7rJkLg6Rvb6hmlO3GKuAACdxIAAscpaUj6aDiZM6SA4jME")
    await message.answer("""Бот находится в разработке и на данный момент он бета-тесте""")
    await message.answer("Привет! Выбери язык, чтобы окунуться в зимний дух торговли!", reply_markup=ikb)


async def cmd_server_selection(callback_query: types.CallbackQuery):  # callback = Russian
    # Выбор языка
    reg(callback_query.from_user.id)
    ikb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    ikb.add(InlineKeyboardButton('RU', callback_data='RU'))
    await bot.send_message(callback_query.from_user.id, "Выберите ваш игровой сервер на этот снегопад❄️:", reply_markup=ikb)


async def cmd_main(callback_query: types.CallbackQuery):  # callback = RU
    await bot.send_message(callback_query.from_user.id, text.WELCOME_TEXT, reply_markup=main_kb)


def register_client_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(cmd_server_selection, text=['Russian'])
    dp.register_callback_query_handler(cmd_main, text=['RU'])
