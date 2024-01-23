import logging

import handlers
from create_bot import create_bot_factory
from create_bot import dp
from database import dbsql
from handlers.admin_handler import content, report, update, result_raffle
from handlers.client_handler import (feedback, start,
                                     get_auc_lot, user_request,
                                     average_price, price_history_chart,
                                     xlsx_table, reboot_cmd,
                                     registration_in_raffle,
                                     boosty)

handlers.client_handler.reboot_cmd.register_client_handler_update(dp)
handlers.client_handler.xlsx_table.register_client_handlers_xlsx_table(dp)
handlers.client_handler.start.register_client_handlers_start(dp)
handlers.client_handler.feedback.register_client_handlers_feedback(dp)
handlers.client_handler.get_auc_lot.register_client_handlers_get_auc_lot(dp)
handlers.client_handler.user_request.register_client_handlers_user_request(dp)
handlers.client_handler.average_price.register_client_handlers_average_price(dp)
handlers.client_handler.price_history_chart.register_client_handlers_price_history_chart(dp)
# handlers.client_handler.registration_in_raffle.register_client_handlers_registration_in_raffle(dp) (Убрал)
handlers.client_handler.boosty.register_client_handlers_boosty(dp)
handlers.admin_handler.report.register_admin_handler_report(dp)
handlers.admin_handler.content.register_admin_handler_content(dp)
handlers.admin_handler.update.register_admin_handler_update(dp)
# handlers.admin_handler.result_raffle.register_admin_handler_result_raffle(dp) (Убрал)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbsql.create_table()
    create_bot_factory()
