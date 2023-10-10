import json

import aiohttp

import database.dbitem
import text
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS, first_querystring
from text import text_auc_lot


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
    page = int(data[1])
    item_id = data[2]
    change = data[0]
    if change == 'remove_page':
        page -= 2

    querystring_auc = {"limit": "10",
                       "sort": "buyout_price",
                       "offset": f"{str(10 * page)}",
                       "order": f"{data[3]}",
                       "additional": "true"}

    data = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(item_id), HEADERS, params=querystring_auc)
    data = json.loads(data)
    lots = data["lots"]
    text_msg = ''

    if database.dbitem.is_it_artifact(item_id):
        for lot in lots:
            text_msg += text_auc_lot.format(lot["amount"], '{0:,}'.format(int(lot["startPrice"])).replace(',', '.'),
                                            '{0:,}'.format(int(lot["buyoutPrice"])).replace(',', '.'),
                                            lot["endTime"][:10], lot["endTime"][11:19])
            try:
                text_msg += f"Качество артефакта: {text.QUALITY[lot['additional']['qlt']]} \n"
            except Exception:
                pass
    else:
        for lot in lots:
            text_msg += text_auc_lot.format(lot["amount"], lot["startPrice"], lot["buyoutPrice"],
                                            lot["endTime"][:10], lot["endTime"][11:19])

    if not text_msg:
        return False, 'Даного предмета нету на аукционе('

    if change == "add_page":
        page += 1
        return len(lots) < 10 or (int(data['total']) // 10) == page, text_msg
    else:
        return False, text_msg


async def get_auc_item_first(id_item: str) -> str:
    """
    :param id_item: id предмета
    :return: Список выбранных предметов с аукциона
    """
    url = f"https://eapi.stalcraft.net/ru/auction/{id_item}/lots"
    data = await make_http_get_request(url, HEADERS, params=first_querystring)
    text_msg = ''
    data = json.loads(data)
    lots = data["lots"] # KeyError: 'lots'

    if database.dbitem.is_it_artifact(id_item):
        for lot in lots:
            text_msg += text_auc_lot.format(lot["amount"], '{0:,}'.format(int(lot["startPrice"])).replace(',', '.'),
                                            '{0:,}'.format(int(lot["buyoutPrice"])).replace(',', '.'),
                                            lot["endTime"][:10], lot["endTime"][11:19])
            try:
                text_msg += f"Качество артефакта: {text.QUALITY[lot['additional']['qlt']]} \n"
            except Exception:
                pass
    else:
        for lot in lots:
            text_msg += text_auc_lot.format(lot["amount"], lot["startPrice"], lot["buyoutPrice"],
                                            lot["endTime"][:10], lot["endTime"][11:19])

    if text_msg:
        pass
    else:
        return 'Даного предмета нету на аукционе('
    return text_msg
