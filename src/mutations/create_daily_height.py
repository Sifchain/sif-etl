from psycopg2 import InterfaceError
import logging
from time import sleep
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_daily_height_mutation", formatter)


def create_daily_height_mutation():
    try:
        sql_str = """
        truncate prices_daily_height
        """
        database_service.execute_update(sql_str)

        sql_str = """
        insert into prices_daily_height 
        (last_height) 
        select max(height) from 
        tokenprices 
        group by date_trunc('day', time)
        """
        database_service.execute_update(sql_str)

    except InterfaceError as exc:
        logger.info(f"Connection problem: {exc}")
        logger.info(f"Trying to sleep it off for 5 minutes")
        sleep(300)
        database_service.execute_query("select 1=1")
