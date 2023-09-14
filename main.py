import logging

import handlers
from create_bot import create_bot_factory
from create_bot import dp
from database import dbsql
from handlers.admin_handler import content, report
from handlers.client_handler import feedback, start, get_auc_lot, user_request

handlers.client_handler.start.register_client_handlers_start(dp)
handlers.client_handler.feedback.register_client_handlers_feedback(dp)
handlers.client_handler.get_auc_lot.register_client_handlers_get_auc_lot(dp)
handlers.client_handler.user_request.register_client_handlers_user_request(dp)
handlers.admin_handler.report.register_admin_handler_report(dp)
handlers.admin_handler.content.register_admin_handler_content(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbsql.create_table()
    create_bot_factory()
