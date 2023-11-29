import json
import aiohttp
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS, first_querystring


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

    querystring_auc = {"limit": "5",
                       "sort": "buyout_price",
                       "offset": f"{str(5 * page)}",
                       "order": f"{data[3]}",
                       "additional": "true"}

    data = await make_http_get_request(URL_GET_ACTIVE_AUC_LOTS.format(item_id), HEADERS, params=querystring_auc)
    data = json.loads(data)
    lots = data["lots"]

    if change == "add_page":
        page += 1
        return data['total'] <= page * 5, lots
    else:
        return False, lots


async def get_auc_item_first(id_item: str) -> str:
    """
    :param id_item: id предмета
    :return: Список выбранных предметов с аукциона
    """
    url = f"https://eapi.stalcraft.net/ru/auction/{id_item}/lots"
    data = await make_http_get_request(url, HEADERS, params=first_querystring)
    data = json.loads(data)
    try:
        lots = data["lots"]
        return lots
    except Exception:
        await get_auc_item_first(id_item)
