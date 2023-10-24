import logging

import handlers
from create_bot import create_bot_factory
from create_bot import dp
from database import dbsql
from handlers.admin_handler import content, report, update
from handlers.client_handler import feedback, start, get_auc_lot, user_request, average_price, price_history_chart

handlers.client_handler.start.register_client_handlers_start(dp)
handlers.client_handler.feedback.register_client_handlers_feedback(dp)
handlers.client_handler.get_auc_lot.register_client_handlers_get_auc_lot(dp)
handlers.client_handler.user_request.register_client_handlers_user_request(dp)
handlers.client_handler.average_price.register_client_handlers_average_price(dp)
handlers.client_handler.price_history_chart.register_client_handlers_price_history_chart(dp)
handlers.admin_handler.report.register_admin_handler_report(dp)
handlers.admin_handler.content.register_admin_handler_content(dp)
handlers.admin_handler.update.register_admin_handler_update(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbsql.create_table()
    create_bot_factory()
