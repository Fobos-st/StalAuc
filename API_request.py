import aiohttp
import json
from config import HEADERS, URL_GET_ACTIVE_AUC_LOTS
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


async def get_auc_item_test(data) -> str:
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
