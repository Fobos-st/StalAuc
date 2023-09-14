import logging
import handlers.client_handler.feedback
from database import dbsql
from create_bot import create_bot_factory
from handlers.client_handler import feedback, start, get_auc_lot
from create_bot import dp


handlers.client_handler.start.register_client_handlers_start(dp)
handlers.client_handler.feedback.register_client_handlers_feedback(dp)
handlers.client_handler.get_auc_lot.register_client_handlers_get_auc_lot(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbsql.create_table()
    create_bot_factory()
