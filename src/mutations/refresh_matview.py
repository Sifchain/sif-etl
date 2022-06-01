import logging
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "refresh_matview_mutation", formatter)


def refresh_matview_mutation():

    logger.setLevel(logging.DEBUG)

    sql_str = """
        refresh materialized view concurrently
        public.spikedrowan_for_tc
        with data;
    """
   # database_service.execute_update(sql_str)

    sql_str = """
        refresh materialized view concurrently
        public.spikedrowan
        with data;
    """
   # database_service.execute_update(sql_str)

    sql_str = """
        refresh materialized view concurrently
        public.mv_token_price_hourly
        with data;
    """
    database_service.execute_update(sql_str)
