import logging
from DataBase.sqlite import create_table
from DataBase.dbitem import open_database
from create_bot import create_bot_factory


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    create_table()
    item_db_ru = open_database()
    create_bot_factory()
