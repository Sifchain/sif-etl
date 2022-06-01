from time import sleep
import logging
from resolvers.refresh_token_registry import refresh_token_registry_resolver
from utils import setup_logger_util
from services import coinmarketcap_service

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_cmc_price_continuous", formatter)


def add_cmc_price_continuous_resolver():
    cnt = 0
    while (True):
        cnt += 1
        try:
            if cnt == 10:
                cnt = 0
                refresh_token_registry_resolver()
            # This needs to be called whenever we add new tokens - every hour?
            coinmarketcap_service.add_cmc_database()
            logger.info(f"PROCESSED CMC PRICES...sleeping for 5 mins")
        except Exception as e:
            errormsg = str(e)
            if errormsg.endswith('closed'):
                raise Exception("Closed!")
            logger.info(f"Error on CMC add {e}")
        sleep(300)
