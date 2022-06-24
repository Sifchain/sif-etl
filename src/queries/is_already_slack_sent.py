import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("is_slack_sent_query", formatter)


def is_already_slack_sent_query(message, recipient):
    sql_str = """
        select notification_id, max(sent_on) as last_sent from notifications_status ns 
        inner join notifications n on n.id = ns.notification_id
        where ns.message = '{0}'
        and n.destination = '{1}'
        group by notification_id
    """.format(message, recipient)

    try:
        rs = database_service.execute_query(sql_str)[0]
        notification_id = rs['notification_id']
        last_sent = rs['last_sent']
        logger.info(f"Notification: {notification_id}, {last_sent}")

        sql_str = """
        select 1 from notifications_status ns 
        where ns.message <> '{0}'
        and ns.notification_id = '{1}'
        and sent_on >= '{2}'
        """.format(message, notification_id, last_sent)

        try:
            database_service.execute_scalar(sql_str)
            return False
        except Exception:
            return True

    except Exception:
        # does not exist so slack was not sent
        return False
