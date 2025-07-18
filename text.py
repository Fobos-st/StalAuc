from database.dbsql import get_request_user
from database.dbitem import search_item_name_by_id, is_it_artifact
import linecache
import sys


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


text_auc_lot = """
Количество: {}
Ставка: {}
Цена выкупа: {}
Время окончание лота: {} {}
"""

notification_text = """
Привет Сталкер, по твоему запросу на ауционе появился предмет❄️
Имя предмета: {} 
Цена выкупа: {}
"""

QUALITY = ("Обычный", "Необычный", "Особый", "Редкий", "Исключительный", "Легандарный")
QUALITY_AVERAGE_PRICE = ("Обычный:", "Необычный:", "Особый:", "Редкий:", "Исключительный:", "Легандарный:")
TIER_AVERAGE_PRICE = [
    "    Неизученый: {}",
    "    С 0 по 4 тир: {}",
    "    5 тир: {}",
    "    С 6 по 9 тир: {}",
    "    10 тир: {}",
    "    С 11 по 14 тир: {}",
    "    15 тир: {}"
]

input_item_name_messeage = 'Введите название предмета, соблюдая язык и правильно название(не обязательно писать полное)'

text_get_curent_lot_artefact = """
Предмет: {}
Цена: от {} и меньше
Качество: от '{}' и более
Заточка: {}
"""

text_get_curent_lot = """
Текущий запрос:
предмет: {}
цена: {}
"""


def current_request(user_id: int) -> str:
    data = get_request_user(user_id)
    if data[1] == 'None':
        return "У вас нету запросов"
    elif is_it_artifact(data[1]):
        return text_get_curent_lot_artefact.format(
            search_item_name_by_id(data[1]),
            data[2],
            QUALITY[int(data[3])],
            "Любая" if data[4] == "All" else data[4])
    else:
        return text_get_curent_lot.format(
            search_item_name_by_id(data[1]),
            data[2]
        )


average_price_artifact = """
Средняя цена за последние 7 дней
Обычный: {}
Необычный: {}
Особый: {}
Редкий: {}
Исключительный: {}
Легендарный: {}
"""

artefact_value = {
    0: [0, 50],
    1: [100, 10],
    2: [110, 10],
    3: [120, 10],
    4: [130, 10],
    5: [140, 10]
}

average_price_artifact_start = """
Средняя цена за '{}' {}
"""

get_and_average_price_artifact = {
    1: 'день',
    3: 'дня',
    7: 'дней',
    4: 'дней'
}

additional_features = {
    "RADIATION_ACC": "-Радиация",
    "PSYCHO_ACC": "-Пси.излучение",
    "MAX_WEIGHT_BONUS": "+Вес",
    "THERMAL_ACC": "-Температура",
    "HEALTH_BONUS": "+Живучесть",
    "REGENERATION_BONUS": "+Регенерация",
    "SPEED_MOD": "+Скорость",
    "STAMINA_BONUS": "+Выносливость",
    "STAMINA_REGENERATION": "+Восст.Выносливости",
    "REACTION_TO_BURN": "+Реакция на ожог",
    "REACTION_TO_ELECTROSHOCK": "Реакция на электро",
    "HEAL_EFFICIENCY": "Эффективка лечения",
    "EXPLOSION_DMG": "+Защита от взрыва",
    "BULLET_DMG": "+Пулестойкость",
    "BIOLOGICAL_ACC": "-Био",
    "THERMAL_DAMAGE_PROTECTION": "Сопр-температуре",
    "BLEEDING_ACC": "-Кровотечение",
    "REACTION_TO_TEAR": "Реакция.разрыв",
    "RADIATION_DAMAGE_PROTECTION": "Защита от рады",
    "PSYCHO_DAMAGE_PROTECTION": "Защита от пси",
    "BIOLOGICAL_DAMAGE_PROTECTION": "Защита от био",
    "TEAR_DMG": "+Защита от разрыва",
    "REACTION_TO_CHEMICAL_BURN": " Реакция хим.ожог"
}

WELCOME_TEXT = """

В этот холодный зимний день, я расскажу тебе о чудесном боте, который словно сказочный артефакт из твоих снов, наполненный зимней атмосферой зоны!
  
В этом боте ты найдешь 2 волшебные кнопки:  
1)❄️Аукцион: В ней ты сможешь получить доступ 3 возможностям:
    Просмотр лота: Чудесная возможность всегда знать что происходит на аукционе не имея под рукой ПДА.

    Средняя цена: Прекрасная возможность узнать среднюю цену торгов предмета на аукциона за последние 7дней\500продаж.

    График цен: Мощный инструмент для опытных экономистов для которых графики свечевые и линейные графики не страшны.

2)🎄Лот-уведомление: 
    Эта функция позволяет добавить уведомление на появление нужного предмет. по нужным для тебя характеристикам и цене.  
Как только он появится на аукционе, бот превратится в маленького помощника санты!🍩 и уведомит тебя об этом.
Главное загадать этот предмет и верить в новогодние чудо.  
  
Этот волшебный бот призван принести в твою жизнь сказочную атмосферу и радость, свойственную зимнему празднику, самое главное не забывать о том что волшебство существует!🍾
"""

appened_user_request = """
Предмет внесён в список
Предмет: {}
Цена: от {} и меньше
"""

appened_user_request_artefact = """
Предмет внесён в список
Предмет: {}
Цена: от {} и меньше
Качество: от '{}' и более
Заточка: {}
"""


joke_text = [
    "Что желаете узнать?",
    "Чего желаете? \nНадеюсь не сахар посмотреть, а то Зив не говорит что там с сахаром",
    "Доброго, чего желаете? \nЛишь бы не ключи смотреть, Зив как обычно жмотит информацию",
    "Вам как обычно?",
    "Хохо, рад вас видеть!\nЧего желаете узнать?",
    "Опять Зив напился, вся база данных с кейсами пропала"
]
