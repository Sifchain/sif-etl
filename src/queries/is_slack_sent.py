import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("is_slack_sent_query", formatter)


def is_slack_sent_query(message_type, recipient):

    sql_str = """
        select * from notifications n inner join notifications_status ns on n.id = ns.notification_id
        where n.notification_type = '{0}'
        and n.destination = '{1}'
        and date_trunc('day', ns.sent_on) >= (select max(date_trunc('day',timestamp)) from pre_distribution_v2 pd2 )
    """.format(message_type, recipient)

    logger.info(sql_str)
    check = database_service.execute_query(sql_str)
    return len(check) > 0
