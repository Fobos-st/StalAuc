import asyncio
import json
import math
import linecache
import sys
from datetime import datetime

from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked

from API_request import make_http_get_request
from config import get_headers, URL_GET_ACTIVE_AUC_LOTS, PARAMS_CHECK_ANY_TIME, BOT_TOKEN
from database import dbitem
from database.dbsql import print_all_users
from text import notification_text
from handlers.keyboard import main_kb

bot = Bot(BOT_TOKEN)


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


async def get_lots_item(item_id, user):
    result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                         head=get_headers(),
                                         params=PARAMS_CHECK_ANY_TIME)
    data_item = json.loads(result)
    try:
        if 'lots' in data_item:
            return data_item
    except KeyError:
        await asyncio.sleep(5)
        await get_lots_item(item_id, user)


async def get_lots_item_more_200(item_id, user, iteration):
    PARAMS_CHECKED = {"limit": "200", "sort": "buyout_price", "additional": "true",
                      "offset": f"{str(iteration * 200)}", "order": "asc"}
    result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                         head=get_headers(),
                                         params=PARAMS_CHECKED)
    data_item = json.loads(result)
    try:
        if 'lots' in data_item:
            return data_item
    except KeyError:
        await asyncio.sleep(5)
        await get_lots_item_more_200(item_id, user, iteration)


async def checking_conditions(user: tuple, lot: dict) -> bool:
    param1 = False
    param2 = False
    param3 = False
    if int(user[2]) >= lot["buyoutPrice"] > 0:
        param1 = True
    try:
        if int(user[3]) <= int(lot["additional"]['qlt']):
            param2 = True
    except ValueError:
        if user[3] == 'None':
            param2 = True
    except KeyError:
        if user[4] == 'All':
            param3 = True

    try:
        if int(user[4]) <= lot["additional"]['ptn']:
            param3 = True
    except ValueError:
        if user[4] == 'All':
            param3 = True
    except KeyError:
        if user[4] == 'All':
            param3 = True

    return param1 and param2 and param3


def remaining_time(time_str):
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    current_time = datetime.utcnow()
    target_time = datetime.strptime(time_str, time_format)
    remaining_time = target_time - current_time

    if remaining_time.days < 0:
        return True
    return False


async def check_item_rework() -> None:
    spam_message = []  #  Список которых хранит инфу уже отправленных лотов пользователям
    """
    Проверяет каждые 2,5 минуты аукцион по запросам пользователей
    В случае наличия нужного предмета отправляет сообщение о его наличие
    Работает в качестве фонового процесса
    :return:
    """
    while True:
        print("начало проверки")
        try:
            users = await print_all_users()
            for user in users:
                    if user[1] == 'None':  # Проверка на наличие зароса у пользователя
                        continue
                    result = await get_lots_item(user[1], user)
                    lots = result['lots']
                    for lot in lots:
                        if lot["buyoutPrice"] < user[2]:  # Скип проверки если цена лота больше запроса пользователя
                            if await checking_conditions(user, lot) and [user[0], lot["endTime"], lot["itemId"]] not in spam_message:
                                try:
                                    await bot.send_message(user[0],
                                                           notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                                           '{0:,}'.format(lot["buyoutPrice"])),
                                                           reply_markup=main_kb)
                                    spam_message.append([user[0], lot["endTime"], lot["itemId"]])
                                    continue
                                except ChatNotFound:
                                    pass
                                except UserDeactivated:
                                    pass
                                except BotBlocked:
                                    pass
                        else:
                            break

                    if int(result['total']) > 200:  # KeyError Ошибка с total
                        iteration = 1
                        count_iteration = math.ceil(int(result['total']) / 200)
                        while iteration <= count_iteration:
                            result = await get_lots_item_more_200(user[1], user, iteration)
                            lots = result['lots']
                            for lot in lots:
                                if lot["buyoutPrice"] < user[2]:
                                    if await checking_conditions(user, lot) and [user[0], lot["endTime"], lot["itemId"]] not in spam_message:
                                        try:
                                            await bot.send_message(user[0],
                                                                   notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                                                   '{0:,}'.format(lot["buyoutPrice"])),
                                                                   reply_markup=main_kb)
                                            spam_message.append([user[0], lot["endTime"], lot["itemId"]])
                                            continue
                                        except ChatNotFound:
                                            pass
                                        except UserDeactivated:
                                            pass
                                        except BotBlocked:
                                            pass
                            iteration += 1

            if sys.getsizeof(spam_message) >= 1048576:
                spam_message = []
            for i in range(len(spam_message)):
                if remaining_time(spam_message[i][1]):
                    spam_message.remove(spam_message[i])

            await asyncio.sleep(35)

        except Exception:
            await bot.send_message(1254191582, PrintException())
            continue
