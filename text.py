from DataBase.sqlite import get_request_user
from DataBase.dbitem import search_item_name_by_id


text_auc_lot = """
Количество: {}
Ставка: {}
Цена выкупа: {}
Время окончание лота: {} {}
"""

notification_text = """
Привет Сталкер, по твоему запросу на ауционе появился предмет
Имя предмета: {} 
Цена выкупа: {}
"""

QUALITY = ("Обычный", "Необычный", "Особый", "Редкий", "Исключительный")


def current_request(user_id: int) -> str:
    data = get_request_user(user_id)
    if data[1] == 'None':
        return "У вас нету запросов"
    text = f"""
Текущий запрос:
предмет: {search_item_name_by_id(data[1])}
цена: {data[2]} \n"""
    if data[3] != 'None':
        text += f"Качество: {QUALITY[int(data[3])]} \n"
    if data[4] == "All":
        text += "Уровень заточки: Любой"
    else:
        text += f"Уровень заточки: {data[4]}"
    return text
