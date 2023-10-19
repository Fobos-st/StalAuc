import json


def open_database_sc() -> dict:
    """
    :return: Выводит список предметов из БД
    """
    with open('database/stalcraft-database/ru/listing.json', "rb") as json_file:
        item_db = json.load(json_file)
        return item_db


def search_item_id_by_name(my_item_name: str, user_lang) -> dict:
    """
    :param my_item_name: Название предмета
    :param user_lang: Язык пользователя
    :return: Предметы с их id
    """
    my_item_name = my_item_name.lower()
    item_db = open_database_sc()
    names_dict = {}
    for a in item_db:
        item_name_ru = a["name"]["lines"]["ru"]
        item_name_en = a["name"]["lines"]["en"]
        if my_item_name.lower() in item_name_ru.lower():
            if user_lang.lower() == 'ru':
                names_dict[item_name_ru] = a["data"].split("/")[-1][:-5]
            else:
                names_dict[item_name_en] = a["data"].split("/")[-1][:-5]
    return names_dict


def get_item_image(my_item_id: str) -> str:
    """
    :param my_item_id: id предмета
    :return: место хранения изображения предмета
    """
    item_db = open_database_sc()
    pris = "ru"
    for a in item_db:
        item_id = a["data"].split("/")[-1][:-5]
        if item_id == my_item_id:
            return "database/stalcraft-database/" + pris + a["icon"]


def is_it_artifact(my_item_id: str) -> bool:
    """
    :param my_item_id: id предмета
    :return: Являеться ли прдемет артефактом
    """
    name = get_item_image(my_item_id)
    status = name.split("/")[4]
    if status == "artefact":
        return True
    else:
        return False


def search_item_name_by_id(my_item_id: str) -> str:
    """
    :param my_item_id: id предмета
    :return: название предмета
    """
    item_db = open_database_sc()
    for a in item_db:
        item_id = a["data"].split("/")[-1][:-5]
        if item_id == my_item_id:
            return a["name"]["lines"]["ru"]
