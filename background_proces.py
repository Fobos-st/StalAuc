import asyncio
import json
import math
import sys

from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked

from API_request import make_http_get_request
from config import BOT_TOKEN
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS, PARAMS_CHECK, PARAMS_CHECK_MORE_200_LOTS
from database import dbitem
from database.dbsql import print_all_users
from text import notification_text

bot = Bot(BOT_TOKEN)


async def get_lots_item(item_id, user):
    result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                         head=HEADERS,
                                         params=PARAMS_CHECK)
    data_item = json.loads(result)
    try:
        if 'lots' in data_item:
            return data_item
    except KeyError:
        await asyncio.sleep(5)
        await get_lots_item(item_id, user)


async def get_lots_item_more_200(item_id, user, iteration):
    PARAMS_CHECKED = {"limit": "200", "sort": "buyout_price", "additional": "true",
                      "offset": f"{str(iteration * 200)}"}
    result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                         head=HEADERS,
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


async def check_item_rework() -> None:
    spam_message = []
    """
    Проверяет каждые 2,5 минуты аукцион по запросам пользователей
    В случае наличия нужного предмета отправляет сообщение о его наличие
    Работает в качестве фонового процесса
    :return:
    """
    while True:
        print("начало проверки")
        users = await print_all_users()

        for user in users:
            try:
                if user[1] == 'None':
                    continue
                result = await get_lots_item(user[1], user)
                lots = result['lots']
                for lot in lots:
                    if await checking_conditions(user, lot) and (user[0], lot["startTime"], lot["itemId"]) not in spam_message:
                        try:
                            await bot.send_message(user[0],
                                                   notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                                                            lot["buyoutPrice"]))
                            spam_message.append((user[0], lot["startTime"], lot["itemId"]))
                            continue
                        except ChatNotFound:
                            pass
                        except UserDeactivated:
                            pass
                        except BotBlocked:
                            pass

                if int(result['total']) > 200:  # KeyError Ошибка с total
                    iteration = 1
                    count_iteration = math.ceil(int(result['total']) / 200)
                    while iteration <= count_iteration:
                        result = await get_lots_item_more_200(user[1], user, iteration)
                        lots = result['lots']
                        for lot in lots:
                            if await checking_conditions(user, lot) and (user[0], lot["startTime"], lot["itemId"]) not in spam_message:
                                try:
                                    await bot.send_message(user[0],
                                                           notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                                                                    lot["buyoutPrice"]))
                                    spam_message.append((user[0], lot["startTime"], lot["itemId"]))
                                    continue
                                except ChatNotFound:
                                    pass
                                except UserDeactivated:
                                    pass
                                except BotBlocked:
                                    pass
                        iteration += 1
            except Exception as ex:
                await bot.send_message(1254191582, ex)
        print("Конец проверки")
        if sys.getsizeof(spam_message) >= 16777216:
            spam_message = []
        await asyncio.sleep(60)
