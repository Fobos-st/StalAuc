import json
from datetime import datetime, timedelta
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import API_request
from aiogram.types import ChatActions
import database.dbitem
import handlers.keyboard
from text import average_price_artifact, input_item_name_messeage
from API_request import make_http_get_request
from config import HEADERS
from create_bot import bot
from ..keyboard import cancel_inline_keyboard


class ItemName(StatesGroup):
    text = State()


async def check_time(time: str) -> bool:
    now = datetime.utcnow()  # Получение текущего времени
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")  # Преобразование строки времени в объект datetime
    diff = now - time  # Вычисление разницы между текущим временем и заданным временем
    if diff <= timedelta(days=7):  # Проверка, что разница не превышает 1 неделю (7 дней)
        return True
    else:
        return False


async def get_auction_average_price(item_id) -> str:
    try:
        item_id = list(item_id.values())[0]
    except AttributeError:
        ...
    max_iteration = 3
    if database.dbitem.is_it_artifact(item_id):
        sum_items = [0, 0, 0, 0, 0, 0]
        count_items = [0, 0, 0, 0, 0, 0]
        for a in range(max_iteration):
            try:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            except AttributeError:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            params = {"limit": "100", "additional": "true", "offset": f"{a * 100}"}
            data = await make_http_get_request(url, HEADERS, params)
            data = json.loads(data)
            lots = data['prices']  # KeyError: 'lots'
            for lot in lots:
                if await check_time(lot['time']):
                    try:
                        count_items[int(lot['additional']['qlt'])] += lot['amount']
                        sum_items[int(lot['additional']['qlt'])] += lot['price']
                    except KeyError:
                        print(lot)
                else:
                    break
        result1 = '{0:,}'.format(int(sum_items[0] / count_items[0])).replace(',', '.') if sum_items[0] != 0 else 'Не было продаж'
        result2 = '{0:,}'.format(int(sum_items[1] / count_items[1])).replace(',', '.') if sum_items[1] != 0 else 'Не было продаж'
        result3 = '{0:,}'.format(int(sum_items[2] / count_items[2])).replace(',', '.') if sum_items[2] != 0 else 'Не было продаж'
        result4 = '{0:,}'.format(int(sum_items[3] / count_items[3])).replace(',', '.') if sum_items[3] != 0 else 'Не было продаж'
        result5 = '{0:,}'.format(int(sum_items[4] / count_items[4])).replace(',', '.') if sum_items[4] != 0 else 'Не было продаж'
        result6 = '{0:,}'.format(int(sum_items[5] / count_items[5])).replace(',', '.') if sum_items[5] != 0 else 'Не было продаж'
        return average_price_artifact.format(result1, result2, result3, result4, result5, result6)
    else:
        sum_items = 0
        count_items = 0
        for a in range(max_iteration):
            try:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            except AttributeError:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            params = {"limit": "100", "additional": "true", "offset": f"{a * 100}"}
            data = await make_http_get_request(url, HEADERS, params)
            data = json.loads(data)
            lots = data['prices']  # KeyError: 'lots'
            for lot in lots:
                if await check_time(lot['time']):
                    count_items += lot['amount']
                    sum_items += lot['price']
                else:
                    break
            if count_items == 0:
                return "Небыло продаж за последние 7 дней"
            return f"Средняя цена за последние 7 дней: {'{0:,}'.format(int(sum_items / count_items)).replace(',', '.')}"


async def cmd_average(message: types.Message):
    await ItemName.text.set()
    await message.answer(input_item_name_messeage,
                         reply_markup=cancel_inline_keyboard)


async def get_name(message: types.Message, state: FSMContext):
    id_item = database.dbitem.search_item_id_by_name(message.text, "RU")
    print(message.from_user.first_name)
    if len(id_item) > 1:
        kb = await handlers.keyboard.get_keyboard_item(id_item)
        await message.reply('Нашёл несколько вариантов, выберете ниже', reply_markup=kb)
    elif len(id_item) == 1:
        msg1 = await message.answer('Собираю информацию')
        await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
        text_msg = await get_auction_average_price(id_item)
        await bot.send_message(message.from_user.id, text_msg, reply_markup=handlers.keyboard.main_kb)
        await msg1.delete()
        await state.finish()
    else:
        await message.answer('Такого предмета нету в нашем списке, а может быть Зив его куда-то унёс во время Хэллоуинской вечеринки с пивом!🍻')
        await state.finish()


async def selection_item(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "(")
    else:
        await state.finish()
        await callback_query.message.delete()
        text_msg = await get_auction_average_price(callback_query.data)
        await bot.send_message(callback_query.from_user.id, text_msg, reply_markup=handlers.keyboard.main_kb)


def register_client_handlers_average_price(dp: Dispatcher):
    dp.register_message_handler(cmd_average, text='Средняя цена')
    dp.register_message_handler(get_name, state=ItemName.text)
    dp.register_callback_query_handler(selection_item, state=ItemName.text)
