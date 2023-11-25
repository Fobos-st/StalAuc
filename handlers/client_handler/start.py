from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import bot
from database.dbsql import reg
from ..keyboard import main_kb


# @dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           r"CAACAgIAAxkBAAEK0RllYhhasr7rJkLg6Rvb6hmlO3GKuAACdxIAAscpaUj6aDiZM6SA4jME")
    await message.answer("""Бот находится в разработке и на данный момент он бета-тесте""")
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton('Русский', callback_data='Russian'))
    await message.answer("Привет! Выбери язык, чтобы окунуться в зимний дух торговли!", reply_markup=ikb)


# @dp.callback_query_handler(text=['Russian'])
async def cmd_server_selection(callback_query: types.CallbackQuery):
    # language depending on the choice
    reg(callback_query.from_user.id)
    ikb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    ikb.add(InlineKeyboardButton('RU', callback_data='RU'))
    await bot.send_message(callback_query.from_user.id, "Выберите ваш игровой сервер на этот снегопад❄️:", reply_markup=ikb)


# @dp.callback_query_handler(text=['RU'])
async def cmd_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, """
Как-то раз в холодный зимний день, когда природа замерзла в ожидании праздника,я расскажу тебе о чудесном боте, который словно сказочный артефакт из твоих снов, наполненный зимней атмосферой праздника и таинственности.

В этом боте ты найдешь 4 волшебные функции:
1)❄️Проверка цены: она помогает узнать цену на нужные тебе волшебные предметы.
2)🎄Ожидание предмета: эта функция позволяет добавить предмет в ожидание по нужным для тебя характеристикам и цене.
Как только он появится на аукционе, бот превратится в маленького помощника и уведомит тебя о событии,
главное загадать этот предмет и верить в новогодние чудо.
3)⛄История цен: создаёт графики цен продаж волшебных предметов,
как будто таинственные свечи, подаренные самим Дедом Морозом🎅🏻. Ты сможешь выбрать время и изучить каждую свечу и её тень, смотря в неизведанные глубины фитиля.
4)🍪Средняя цена: покажет тебе среднюю цену продажи предмета.

Этот волшебный бот призван принести в твою жизнь сказочную атмосферу и радость, свойственную зимнему празднику, самое главное не забывать о том что волшебство существует!🍾
""", reply_markup=main_kb)


def register_client_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(cmd_server_selection, text=['Russian'])
    dp.register_callback_query_handler(cmd_main, text=['RU'])
