import aiohttp
import json
import asyncio
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS, PARAMS_CHECK, PARAMS_CHECK_MORE_200_LOTS
from text import text_auc_lot, notification_text
from create_bot import bot


async def make_http_get_request(url: str, head: str, params: str):
    """
    Создаёт GET запрос
    :param url: URL-адресс для Запроса
    :param head: TOKEN API и Content-Type
    :param params:
    :return: Результат GET запроса
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=head, params=params) as response:
            return await response.text()


async def get_auc_item(data) -> str:
    """
    :param data: callback данные
    :return: Список выбранных предметов с аукциона
    """
    change = data[0]
    page = int(data[1])
    if change == 'remove_page':
        page -= 2

    querystring_auc = {"limit": "10",
                       "sort": "buyout_price",
                       "offset": f"{str(10 * page)}",
                       "order": f"{data[3]}",
                       "additional": "true"}

    data = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(data[2]), HEADERS, params=querystring_auc)
    data = json.loads(data)
    lots = data["lots"]
    text = ''
    for lot in lots:
        text += text_auc_lot.format(lot["amount"], lot["startPrice"], lot["buyoutPrice"],
                                    lot["endTime"][:10], lot["endTime"][11:19])
    if text:
        pass
    else:
        return False, 'Даного предмета нету на аукционе('
    if change == "add_page":
        page += 1
        return len(lots) < 10 or (int(data['total']) // 10) == page, text
    else:
        print(False, 'text')
        return False, text


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

    try:
        if int(user[4]) <= lot["additional"]['ptn']:
            param3 = True
    except ValueError:
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
                                               notification_text.format(search_item_name_by_id(user[1]),
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
                                                       notification_text.format(search_item_name_by_id(user[1]),
                                                                                lot_more_200["buyoutPrice"]))
                                continue
                            except Exception:
                                pass
        print("Конец проверки")
        await asyncio.sleep(150)
