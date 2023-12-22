from aiogram import Dispatcher, types
from database.dbsql import reg_in_sweepstakes

import database.dbsql


async def send_reg_message(message: types.Message):
    await message.answer(await reg_in_sweepstakes(message.from_user.id, message.from_user.full_name))


def register_client_handlers_registration_in_raffle(dp: Dispatcher):
    dp.register_message_handler(send_reg_message, content_types=['text'], text="Участвовать в розыгрыше")
