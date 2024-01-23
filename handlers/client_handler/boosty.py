from aiogram import Dispatcher, types

import handlers.keyboard
from create_bot import bot


text_boosty = """
Проект очень сильно зависит от будущей подержки как финансовой так и моральной.
Если вам нравится бот и есть желание помочь то я буду рад любой помощи.

Вся сумма будет уходить на оплату хостинга!
https://boosty.to/stalauction_donation
"""


async def send_table(message: types.Message):
    await message.answer(text_boosty, reply_markup=handlers.keyboard.main_kb)


def register_client_handlers_boosty(dp: Dispatcher):
    dp.register_message_handler(send_table, content_types=['text'], text="Финанс.помощь проекту")
