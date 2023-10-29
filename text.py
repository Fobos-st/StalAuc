from database.dbsql import get_request_user
from database.dbitem import search_item_name_by_id


text_auc_lot = """
Количество: {}
Ставка: {}
Цена выкупа: {}
Время окончание лота: {} {}
"""

notification_text = """
Привет Сталкер, по твоему запросу на ауционе появился предмет🎃
Имя предмета: {} 
Цена выкупа: {}
"""

QUALITY = ("Обычный", "Необычный", "Особый", "Редкий", "Исключительный")

input_item_name_messeage = 'Введите название предмета, соблюдая язык и правильно название(не обязательно писать полное)'


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


average_price_artifact = """
Средняя цена за последние 7 дней
Обычный: {}
Необычный: {}
Особый: {}
Редкий: {}
Исключительный: {}
Легендарный: {}
"""


additional_features = {
"RADIATION_ACC" : "-Радиация",
"PSYCHO_ACC" : "-Пси.излучение",
"MAX_WEIGHT_BONUS" : "+Вес",
"THERMAL_ACC" : "-Температура",
"HEALTH_BONUS" : "+Живучесть",
"REGENERATION_BONUS" : "+Регенерация",
"SPEED_MOD" : "+Скорость",
"STAMINA_BONUS" : "+Выносливость",
"STAMINA_REGENERATION" : "+Восст.Выносливости",
"REACTION_TO_BURN" : "+Реакция на ожог",
"REACTION_TO_ELECTROSHOCK" : "Реакция на электро",
"HEAL_EFFICIENCY" : "Эффективка лечения",
"EXPLOSION_DMG" : "+Защита от взрыва",
"BULLET_DMG" : "+Пулестойкость",
"BIOLOGICAL_ACC": "-Био",
"THERMAL_DAMAGE_PROTECTION": "Сопр-температуре"
}
