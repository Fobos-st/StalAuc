import asyncio
import json
import os
from datetime import datetime, timedelta

# import mplfinance as mpf
# import pandas as pd
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from openpyxl import Workbook
from openpyxl.chart import (
    BarChart,
    StockChart,
    Reference,
    LineChart
)
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.updown_bars import UpDownBars
import openpyxl

import database.dbitem
import handlers.keyboard
import text
from API_request import make_http_get_request
from config import URL_GET_HISTORY_AUC_LOTS, get_headers
from create_bot import bot
from ..keyboard import cancel_inline_keyboard
from aiogram.types import ChatActions
HEADERS_LIST = True


class CreateChart(StatesGroup):
    item_id = State()
    days = State()
    timing = State()


async def check_time(time: str, days) -> bool:
    now = datetime.utcnow()  # Получение текущего времени
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")  # Преобразование строки времени в объект datetime
    diff = now - time  # Вычисление разницы между текущим временем и заданным временем
    if diff <= timedelta(days=days):  # Проверка, что разница не превышает 1 неделю (7 дней)
        return True
    else:
        return False


PARAMS_CHECK = {"limit": "200", "sort": "buyout_price", "additional": "true"}


async def get_data_item(item_id):
    data_item = await make_http_get_request(URL_GET_HISTORY_AUC_LOTS.format(item_id), get_headers(), PARAMS_CHECK)
    data_item = json.loads(data_item)
    try:
        data_item = data_item['prices']
    except KeyError:
        await asyncio.sleep(10)
        await get_data_item(item_id)
    return data_item


async def get_data_item_more_200(item_id, iteration):
    params_check_more_200 = {"limit": "200", "sort": "buyout_price", "additional": "true",
                      "offset": f"{str(iteration * 200)}"}
    data_item = await make_http_get_request(URL_GET_HISTORY_AUC_LOTS.format(item_id), get_headers(), params_check_more_200)
    data_item = json.loads(data_item)
    try:
        data_item = data_item['prices']
    except KeyError:
        await asyncio.sleep(10)
        await get_data_item_more_200(item_id, iteration)
    return data_item


async def check_time_passed(start_time, end_time, minutes):
    # Преобразуем строки с временем в объекты datetime
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")

    # Разница во времени между start_time и end_time в минутах
    time_diff = (start_time - end_time).total_seconds() / 60
    # Проверяем, если разница больше или равна заданному количеству минут
    if time_diff >= minutes:
        return True
    else:
        return False


async def parse_json_file_test(days, item_id, minutes):
    data_item = await get_data_item(item_id)
    iteration = 0
    counter = 0
    day = 0
    count = 0

    price_sell = [data_item[counter]["price"] / data_item[counter]["amount"]]
    dates_sold = [data_item[counter]["time"]]
    open_prices = [data_item[counter]["price"] / data_item[counter]["amount"]]
    high_prices = [data_item[counter]["price"] / data_item[counter]["amount"]]
    low_prices = [data_item[counter]["price"] / data_item[counter]["amount"]]
    close_prices = []
    value = [1]
    counter += 1

    while day < days:
        if counter >= 200 or counter >= 200 * (iteration + 1):
            iteration += 1
            data_item = await get_data_item_more_200(item_id, iteration)
            counter = 0
        if await check_time(str(data_item[counter]["time"]), days):
            if await check_time_passed(dates_sold[count], data_item[counter]['time'], minutes):
                dates_sold.append(str(data_item[counter]["time"]))
                open_prices.append(data_item[counter]["price"] / data_item[counter]["amount"])
                high_prices.append(data_item[counter]["price"] / data_item[counter]["amount"])
                low_prices.append(data_item[counter]["price"] / data_item[counter]["amount"])
                close_prices.append(data_item[counter - 1]["price"] / data_item[counter - 1]["amount"])
                value.append(1)
                price_sell.append(data_item[counter]["price"] / data_item[counter]["amount"])
                counter += 1
                count += 1
                continue

            if high_prices[count] < data_item[counter]["price"] / data_item[counter]["amount"]:
                high_prices[count] = data_item[counter]["price"] / data_item[counter]["amount"]
                price_sell.append(data_item[counter]["price"] / data_item[counter]["amount"])
                counter += 1
                value[count] += 1
                continue

            if low_prices[count] > data_item[counter]["price"] / data_item[counter]["amount"]:
                low_prices[count] = data_item[counter]["price"] / data_item[counter]["amount"]
                price_sell.append(data_item[counter]["price"] / data_item[counter]["amount"])
                counter += 1
                value[count] += 1
                continue

            price_sell.append(data_item[counter]["price"] / data_item[counter]["amount"])
            counter += 1
            value[count] += 1
        else:
            close_prices.append(data_item[counter - 1]["price"] / data_item[counter - 1]["amount"])
            return (dates_sold[::-1], open_prices[::-1], high_prices[::-1], low_prices[::-1],
                    close_prices[::-1], value[::-1], price_sell[::-1])


# async def create_table(days, user_id, item_id):
#     mc = mpf.make_marketcolors(
#         up="red",  # Цвет линии K
#         down="green",  # Падение k -Line Color
#         edge="black",  # Цвет кузова коробки для карты свечи
#         volume="blue",  # Цвет стойки объема транзакции
#         wick="black"  # Цвет линии теневой карты свечи.
#     )
#
#     s = mpf.make_mpf_style(
#         marketcolors=mc,
#         figcolor='w',
#         facecolor='w')
#
#     dates_sold, open_prices, high_prices, low_prices, close_prices, value = await parse_json_file(days, item_id)
#
#     data = {'date': dates_sold,
#             'open': open_prices,
#             'high': high_prices,
#             'low': low_prices,
#             'close': close_prices,
#             'volume': value}
#
#     df = pd.DataFrame(data)
#     df['date'] = pd.to_datetime(df['date'])
#     df.set_index('date', inplace=True)
#
#     filename = f'{user_id + days}'
#
#     mpf.plot(df, style=s,
#              title='История цен',
#              xlabel='Даты',
#              ylabel='Цена',
#              ylabel_lower='кл-в продаж',
#              type='candle', mav=(2, 4), volume=True, savefig=filename)
#
#     return filename + '.png'


async def create_table_excel(days, user_id, item_id, minuts):
    dates_sold, open_prices, high_prices, low_prices, close_prices, value, price_list = await parse_json_file_test(days, item_id, minuts)
    rows = []
    for i in range(len(dates_sold)):
        rows.append([])
        rows[i].append(dates_sold[i])
        rows[i].append(value[i])
        rows[i].append(open_prices[i])
        rows[i].append(high_prices[i])
        rows[i].append(low_prices[i])
        rows[i].append(close_prices[i])

    wb = Workbook()
    ws = wb.active

    for row in rows:
        ws.append(row)

    # High-low-close
    c1 = StockChart()
    labels = Reference(ws, min_col=1, min_row=2, max_row=len(dates_sold))
    data = Reference(ws, min_col=4, max_col=6, min_row=1, max_row=len(dates_sold))
    c1.add_data(data, titles_from_data=True)
    c1.set_categories(labels)
    for s in c1.series:
        s.graphicalProperties.line.noFill = True

    # Excel is broken and needs a cache of values in order to display hiLoLines :-/
    from openpyxl.chart.data_source import NumData, NumVal
    pts = [NumVal(idx=i) for i in range(len(data) - 1)]
    cache = NumData(pt=pts)
    c1.series[-1].val.numRef.numCache = cache

    # Open-high-low-close
    c2 = StockChart()
    data = Reference(ws, min_col=3, max_col=6, min_row=1, max_row=len(dates_sold))
    c2.add_data(data, titles_from_data=True)
    c2.set_categories(labels)
    for s in c2.series:
        s.graphicalProperties.line.noFill = True
    c2.hiLowLines = ChartLines()
    c2.upDownBars = UpDownBars()
    c2.title = "Open-high-low-close"

    # add dummy cache
    c2.series[-1].val.numRef.numCache = cache

    ws.add_chart(c2, "G10")

    # Create bar chart for volume

    bar = BarChart()
    data = Reference(ws, min_col=2, min_row=1, max_row=len(dates_sold))
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(labels)

    from copy import deepcopy

    # Volume-high-low-close
    b1 = deepcopy(bar)
    c3 = deepcopy(c1)
    c3.y_axis.majorGridlines = None
    c3.y_axis.title = "Price"
    b1.y_axis.axId = 20
    b1.z_axis = c3.y_axis
    b1.y_axis.crosses = "max"
    b1 += c3

    c3.title = "High low close volume"

    ws.add_chart(b1, "A27")

    filename = str(user_id) + str(days) + item_id
    wb.save(f"{filename}Свечевой.xlsx")

    wb = openpyxl.Workbook()
    sheet = wb.active

    for i in price_list:
        sheet.append([i])

    values = Reference(sheet, min_col=1, min_row=1,
                       max_col=1, max_row=len(price_list))

    # Create object of LineChart class
    chart = LineChart()

    chart.add_data(values)
    chart.title = " График "
    chart.x_axis.title = " Номер продажи "
    chart.y_axis.title = " Цена продажи "
    sheet.add_chart(chart, "E2")
    wb.save(f"{filename}Линейный.xlsx")

    return filename


# @dp.message_handler(text='История цен')
async def cmd_create_chart(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Мини гайд по графику https://youtu.be/UCaeJpC_s4A?si=6BftfsApqzudVzwu, так-же стоит учитывать что создание графика достаточно долгое дело")
    await CreateChart.item_id.set()
    await callback_query.answer('Советую не создавать график с историей цен артефакта(Так как нету сортировки)')
    await bot.send_message(callback_query.from_user.id, text.input_item_name_messeage,
                           reply_markup=cancel_inline_keyboard)
    await callback_query.message.delete()


# @dp.message_handler(content_types=["text"], state=CreateChart.item_id)
async def get_item_id_one(message: types.Message, state: FSMContext):
    id_item = database.dbitem.search_item_id_by_name(message.text, "RU")
    print(message.from_user.first_name)
    if len(id_item) > 1:
        kb = await handlers.keyboard.get_keyboard_item(id_item)
        return await message.reply('Нашёл несколько вариантов, выберете ниже', reply_markup=kb)
    elif len(id_item) == 1:
        id_item = list(id_item.values())[0]
        async with state.proxy() as data:
            data['item_id'] = id_item
        await CreateChart.next()
        await message.answer("За сколько дней вывести информацию? (число от 1 до 31)")
    else:
        await message.answer('Такого предмета нету в нашем списке, а может быть Зив его куда-то унёс во время зимней вечеринки с пивом!🍻',
                             reply_markup=handlers.keyboard.main_kb)
        await state.finish()


# @dp.callback_query_handler(state=CreateChart.item_id)
async def get_item_id_two(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "(", reply_markup=handlers.keyboard.main_kb)
    else:
        await CreateChart.next()
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "За сколько дней вывести информацию? (число от 1 до 31)")
        callback_data = callback_query.data
        id_item = callback_data
        async with state.proxy() as data:
            data['item_id'] = id_item


# @dp.message_handler(state=CreateChart.days)
async def get_count_days(message: types.Message, state: FSMContext):
    try:
        days = int(message.text)
    except ValueError:
        await state.finish()
        return await message.answer('Некоректный ввод данных', reply_markup=handlers.keyboard.main_kb)
    if 0 < days <= 31:
        async with state.proxy() as data:
            data['days'] = days
        await message.answer("Теперь напишите тайминги таблицы(в минутах), советую учитывать ликвидность товара и срок за который выводится информация")
        await message.answer("Напишите число. На выбор от 15 минут до 720минут(12 часов), в ином случае любое другое сообщение и тайминг будет 24часа")
        await CreateChart.next()


# @dp.message_handler(state=CreateChart.timing)
async def get_count_timing(message: types.Message, state: FSMContext):
    try:
        if 15 <= int(message.text) <= 720:
            data = await state.get_data()
            msg = await message.answer('Собираю информцию')
            await asyncio.sleep(int(data['days']) / 10)
            await msg.delete()
            await message.answer('Рисую график')
            await asyncio.sleep(int(data['days']) / 10)
            filename = await create_table_excel(data['days'], message.from_user.id, data['item_id'], int(message.text))
            await bot.send_message(1254191582, filename)
            await state.finish()
            with open(f'{filename}Свечевой.xlsx', 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            with open(f'{filename}Линейный.xlsx', 'rb') as file:
                await bot.send_document(message.from_user.id, file, reply_markup=handlers.keyboard.main_kb)
            os.remove(f'{filename}Линейный.xlsx')
            os.remove(f'{filename}Свечевой.xlsx')
        else:
            data = await state.get_data()
            msg = await message.answer('Собираю информцию')
            await asyncio.sleep(int(data['days']) / 10)
            await msg.delete()
            await message.answer('Рисую график')
            await asyncio.sleep(int(data['days']) / 10)
            filename = await create_table_excel(data['days'], message.from_user.id, data['item_id'], 1440)
            await bot.send_message(1254191582, filename)
            with open(f'{filename}Свечевой.xlsx', 'rb') as file:
                await bot.send_document(message.from_user.id, file)
            with open(f'{filename}Линейный.xlsx', 'rb') as file:
                await bot.send_document(message.from_user.id, file, reply_markup=handlers.keyboard.main_kb)
            os.remove(f'{filename}Линейный.xlsx')
            os.remove(f'{filename}Свечевой.xlsx')
    except ValueError:
        data = await state.get_data()
        await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
        msg = await message.answer('Собираю информцию')
        await asyncio.sleep(int(data['days']) / 10)
        await msg.delete()
        await bot.send_chat_action(message.from_user.id, ChatActions.UPLOAD_DOCUMENT)
        await message.answer('Рисую график')
        await asyncio.sleep(int(data['days']) / 10)
        filename = await create_table_excel(data['days'], message.from_user.id, data['item_id'], 1440)
        await bot.send_message(1254191582, filename)
        await state.finish()
        with open(f'{filename}Свечевой.xlsx', 'rb') as file:
            await bot.send_document(message.from_user.id, file)
        with open(f'{filename}Линейный.xlsx', 'rb') as file:
            await bot.send_document(message.from_user.id, file, reply_markup=handlers.keyboard.main_kb)
        os.remove(f'{filename}Линейный.xlsx')
        os.remove(f'{filename}Свечевой.xlsx')


def register_client_handlers_price_history_chart(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_create_chart, text='auction_chart_price')
    dp.register_message_handler(get_item_id_one, state=CreateChart.item_id)
    dp.register_callback_query_handler(get_item_id_two, state=CreateChart.item_id)
    dp.register_message_handler(get_count_days, state=CreateChart.days)
    dp.register_message_handler(get_count_timing, state=CreateChart.timing)
