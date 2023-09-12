import aiohttp


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
