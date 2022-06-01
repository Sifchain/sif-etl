import logging
from time import sleep
from mutations import refresh_matview_mutation
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_price_record_resolver", formatter)


def add_spiked_cache_resolver():
    while (True):
        try:
            refresh_matview_mutation()
        except Exception as e:
            logger.info(e)
        logger.info("Sleeping for 30 minutes")
        sleep(1800)
