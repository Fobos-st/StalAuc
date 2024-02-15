import asyncio
import json
from json import JSONDecodeError
from datetime import datetime, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ChatActions

import API_request
import database.dbitem
import handlers.keyboard
from API_request import make_http_get_request
from config import URL_GET_HISTORY_AUC_LOTS, PARAMS_CHECK, get_headers
from create_bot import bot
from text import (get_and_average_price_artifact,
                  average_price_artifact_start,
                  QUALITY_AVERAGE_PRICE,
                  TIER_AVERAGE_PRICE,
                  input_item_name_messeage)
from ..keyboard import cancel_inline_keyboard, main_kb, choice_count_days_keyboard


class ItemName(StatesGroup):
    text = State()
    CountDays = State()


async def check_time(time: str, day: int) -> bool:
    now = datetime.utcnow()  # Получение текущего времени
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")  # Преобразование строки времени в объект datetime
    diff = now - time  # Вычисление разницы между текущим временем и заданным временем
    if diff <= timedelta(days=day):  # Проверка, что разница не превышает 1 неделю (7 дней)
        return True
    else:
        return False


async def get_data_item(item_id):
    data_item = await make_http_get_request(URL_GET_HISTORY_AUC_LOTS.format(item_id), get_headers(), PARAMS_CHECK)
    data_item = json.loads(data_item)
    try:
        data_item = data_item['prices']
    except KeyError:
        await asyncio.sleep(10)
        await get_data_item(item_id)
    return data_item


async def get_data_item_more_100(url, params):
    data_item = await make_http_get_request(url, get_headers(), params)
    data_item = json.loads(data_item)
    try:
        data_item = data_item['prices']
    except KeyError:
        await asyncio.sleep(10)
        await get_data_item_more_100(url, params)
    return data_item


async def get_auction_average_price(item_id, count_day) -> str:
    try:
        item_id = list(item_id.values())[0]
    except AttributeError:
        ...
    max_iteration = count_day * 10
    if database.dbitem.is_it_artifact(item_id):
        sum_items = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        count_items = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        for a in range(max_iteration):
            print(1)
            params = {"limit": "100", "additional": "true", "offset": f"{a * 100}"}
            url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            lots = await get_data_item_more_100(url, params)
            for lot in lots:
                if await check_time(lot['time'], count_day):

                    if 'stats_random' not in lot['additional'] and 'ptn' not in lot['additional']:  # Если неизученный
                        try:
                            count_items[lot['additional']['qlt']][0] += lot['amount']
                            sum_items[lot['additional']['qlt']][0] += lot['price']
                        except KeyError:
                            count_items[0][0] += lot['amount']
                            sum_items[0][0] += lot['price']

                    elif 'qlt' not in lot['additional']:  # Если у обычного нету пункта qlt
                        if 'ptn' not in lot['additional'] or 1 >= lot['additional']['ptn'] <= 4:  # С 0 по 4 тир
                            count_items[0][1] += lot['amount']
                            sum_items[0][1] += lot['price']
                        elif lot['additional']['ptn'] == 5:  # 5 тир
                            count_items[0][2] += lot['amount']
                            sum_items[0][2] += lot['price']
                        elif 6 >= lot['additional']['ptn'] <= 9:  # С 6 по 9 тир
                            count_items[0][3] += lot['amount']
                            sum_items[0][3] += lot['price']
                        elif lot['additional']['ptn'] == 10:  # 10 тир
                            count_items[0][4] += lot['amount']
                            sum_items[0][4] += lot['price']
                        elif 11 >= lot['additional']['ptn'] <= 14:  # С 11 по 14 тир
                            count_items[0][5] += lot['amount']
                            sum_items[0][5] += lot['price']
                        elif lot['additional']['ptn'] == 15:  # 15 тир
                            count_items[0][6] += lot['amount']
                            sum_items[0][6] += lot['price']

                    else:  # Если изученный
                        if 'ptn' not in lot['additional'] or 1 >= lot['additional']['ptn'] <= 4:  # С 0 по 4 тир
                            count_items[lot['additional']['qlt']][1] += lot['amount']
                            sum_items[lot['additional']['qlt']][1] += lot['price']
                        elif lot['additional']['ptn'] == 5:  # 5 тир
                            count_items[lot['additional']['qlt']][2] += lot['amount']
                            sum_items[lot['additional']['qlt']][2] += lot['price']
                        elif 6 >= lot['additional']['ptn'] <= 9:  # С 6 по 9 тир
                            count_items[lot['additional']['qlt']][3] += lot['amount']
                            sum_items[lot['additional']['qlt']][3] += lot['price']
                        elif lot['additional']['ptn'] == 10:  # 10 тир
                            count_items[lot['additional']['qlt']][4] += lot['amount']
                            sum_items[lot['additional']['qlt']][4] += lot['price']
                        elif 11 >= lot['additional']['ptn'] <= 14:  # С 11 по 14 тир
                            count_items[lot['additional']['qlt']][5] += lot['amount']
                            sum_items[lot['additional']['qlt']][5] += lot['price']
                        elif lot['additional']['ptn'] == 15:  # 15 тир
                            count_items[lot['additional']['qlt']][6] += lot['amount']
                            sum_items[lot['additional']['qlt']][6] += lot['price']

                else:
                    break
        text = average_price_artifact_start.format(count_day, get_and_average_price_artifact[count_day % 10])
        for i in range(6):
            if sum(count_items[i]) != 0:
                text += QUALITY_AVERAGE_PRICE[i]
                text += '\n'
                for n in range(7):
                    if count_items[i][n] != 0:
                        text += TIER_AVERAGE_PRICE[n].format('{0:,}'.format(int(sum_items[i][n] / count_items[i][n]))) if sum_items[i][n] != 0 else ''
                        text += '\n'
        return text
    else:
        sum_items = 0
        count_items = 0
        stoper = False
        for a in range(max_iteration):
            try:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            except AttributeError:
                url = f"https://eapi.stalcraft.net/ru/auction/{item_id}/history"
            params = {"limit": "100", "additional": "true", "offset": f"{a * 100}"}
            lots = await get_data_item_more_100(url, params)

            for lot in lots:
                if await check_time(lot['time'], count_day):
                    count_items += lot['amount']
                    sum_items += lot['price']
                else:
                    stoper = True
                    print('пиздык')
                    break
            if stoper:
                break
            if count_items == 0:
                return "Небыло продаж за последние 7 дней"

        lots = await API_request.get_auc_item_average_price(item_id)
        if len(lots) != 0:
            counter = 0
            while lots[counter]['buyoutPrice'] == 0:  # скип лотов без цены выкупа
                counter += 1
            current_price = [lots[counter]['buyoutPrice'], 1]
            for i in range(counter + 1, len(lots)):
                if ((lots[i]['buyoutPrice'] - lots[counter]['buyoutPrice']) / (lots[counter]['buyoutPrice'] / 100)) < 4.2:
                    current_price[0] += lots[i]['buyoutPrice']
                    current_price[1] += 1
                elif ((lots[counter + 1]['buyoutPrice'] - lots[counter]['buyoutPrice']) / (lots[counter]['buyoutPrice'] / 100)) > 9:
                    #  Если первый лот сликшом дешёвый в сравнение со следующими то они тоже будут учитываться если
                    #  их разница меньше 3% стоимости

                    if i == counter + 1:
                        #  Скипаю 2 лот
                        continue

                    if ((lots[i]['buyoutPrice'] - lots[1]['buyoutPrice']) / (lots[1]['buyoutPrice'] / 100)) < 3.8:
                        current_price[0] += lots[i]['buyoutPrice']
                        current_price[1] += 1
                        if i == 2:
                            current_price[0] += lots[1]['buyoutPrice']
                            current_price[1] += 1
                    else:
                        break
                else:
                    break
            return f"Средняя цена за '{count_day}' {get_and_average_price_artifact[count_day % 10]}: {'{0:,}'.format(int(sum_items / count_items))} \nКоличество продаж:{count_items}\nАктуальная цена на аукционе: {'{0:,}'.format(int(current_price[0] / current_price[1]))}"
        return f"Средняя цена за '{count_day}' {get_and_average_price_artifact[count_day % 10]}: {'{0:,}'.format(int(sum_items / count_items))} \nКоличество продаж:{count_items} \nАктуальная цена на аукционе: Отсуствует информация"


async def cmd_average(callback_query: types.CallbackQuery):
    await ItemName.text.set()
    await bot.send_message(callback_query.from_user.id, input_item_name_messeage,
                           reply_markup=cancel_inline_keyboard)
    await callback_query.message.delete()


async def get_name(message: types.Message, state: FSMContext):
    id_item = database.dbitem.search_item_id_by_name(message.text, "RU")
    print(message.from_user.first_name)
    if len(id_item) > 1:
        kb = await handlers.keyboard.get_keyboard_item(id_item)
        await message.reply('Нашёл несколько вариантов, выберете ниже', reply_markup=kb)
    elif len(id_item) == 1:
        callback_data = list(id_item.values())[0]
        await state.update_data(text=callback_data)
        await ItemName.next()
        await message.answer("За какой срок времени вывести информацию", reply_markup=choice_count_days_keyboard)
    else:
        await message.answer('Такого предмета нету в нашем списке, а может быть Зив его куда-то унёс во время Зимней вечеринки с пивом!🍻',
                             reply_markup=main_kb)
        await state.finish()


async def get_count_days(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.update_data(text=callback_query.data)
    await ItemName.next()
    await bot.send_message(callback_query.from_user.id, "За какой срок времени вывести информацию",
                           reply_markup=choice_count_days_keyboard)


async def send_average_price(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(CountDays=callback_query.data)
        data = await state.get_data()
        await state.finish()
        await bot.send_chat_action(callback_query.from_user.id, ChatActions.TYPING)
        await callback_query.message.delete()
        text_msg = await get_auction_average_price(data["text"], int(data["CountDays"][3:]))
        await bot.send_message(callback_query.from_user.id, text_msg)
    except JSONDecodeError:
        await bot.send_message(callback_query.from_user.id, "К сожалению возникла ошибка при работе с вашим запросом")


def register_client_handlers_average_price(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_average, text='auction_average_price')
    dp.register_message_handler(get_name, content_types=["text"], state=ItemName.text)
    dp.register_callback_query_handler(get_count_days, state=ItemName.text)
    dp.register_callback_query_handler(send_average_price, state=ItemName.CountDays)
