from aiogram import Dispatcher, types

import handlers.keyboard
from create_bot import bot


async def send_table(message: types.Message):
    await message.answer("Таблицы сами за тебя всё подсчитают, ты лишь вводи значения в нужные столбцы и радуйся профиту",
                         reply_markup=handlers.keyboard.main_kb)
    with open("handlers\client_handler\Перекуп Таблица.xlsx", 'rb') as file:
        await bot.send_document(message.from_user.id, file)


def register_client_handlers_xlsx_table(dp: Dispatcher):
    dp.register_message_handler(send_table, content_types=['text'], text="Перкуп таблица")
