from aiogram import Dispatcher, types

from handlers.keyboard import (auction_choice_keyboard,
                               background_process_choice_keyboard_0,
                               background_process_choice_keyboard_1)
from database.dbsql import check_user_request_lot
from text import current_request


async def send_auction_choice(message: types.Message):
    await message.answer("Text auction", reply_markup=auction_choice_keyboard)


async def send_background_process_choice(message: types.Message):
    #  Добавит проверку из бд и выводить инфу об текущем лоте юзера
    if check_user_request_lot(message.from_user.id):
        await message.answer(text="Text background_process", reply_markup=background_process_choice_keyboard_0)
    else:
        await message.answer(text=f"Ваш текущий лот: \n {current_request(message.from_user.id)}",
                             reply_markup=background_process_choice_keyboard_1)


def register_client_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(send_auction_choice, content_types=['text'], text="Аукцион")
    dp.register_message_handler(send_background_process_choice, content_types=['text'], text="Лот-уведомление")
