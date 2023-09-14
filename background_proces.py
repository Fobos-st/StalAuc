import asyncio
import json

from aiogram import Bot

from API_request import make_http_get_request
from config import BOT_TOKEN
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS, PARAMS_CHECK, PARAMS_CHECK_MORE_200_LOTS
from database import dbitem
from database.dbsql import print_all_users
from text import notification_text

bot = Bot(BOT_TOKEN)


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


async def check_item() -> None:
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
            if user[1] == 'None':
                continue
            result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                                 head=HEADERS,
                                                 params=PARAMS_CHECK)
            result = json.loads(result)
            lots = result["lots"]
            for lot in lots:
                if await checking_conditions(user, lot):
                    try:
                        await bot.send_message(user[0],
                                               notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                               lot["buyoutPrice"]))
                        continue
                    except Exception:
                        pass
                if int(result['total']) > 200:
                    result = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(user[1]),
                                                         head=HEADERS,
                                                         params=PARAMS_CHECK_MORE_200_LOTS)
                    result = json.loads(result)
                    for lot_more_200 in lots:
                        if await checking_conditions(user, lot):
                            try:
                                await bot.send_message(user[0],
                                                       notification_text.format(dbitem.search_item_name_by_id(user[1]),
                                                                                lot_more_200["buyoutPrice"]))
                                continue
                            except Exception:
                                pass
        print("Конец проверки")
        await asyncio.sleep(150)
