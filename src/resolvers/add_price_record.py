from datetime import datetime, timezone

from src.mutations.create_price_record import create_price_record_mutation
from src.queries.get_token_volumes import get_token_volumes_query
from src.services.sifapi import *
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_price_record_resolver", formatter)


def add_price_record_resolver():
    current_time = datetime.now(timezone.utc)

    try:
        (token_prices_dict, rowan_cusdt, height,
         timestamp) = get_price_records_sifapi()
        token_volumes_dict = get_token_volumes_query()
        create_price_record_mutation(height, timestamp, rowan_cusdt,
                                     token_prices_dict, token_volumes_dict)
    except Exception as e:
        errormsg = str(e)
        if errormsg.endswith("closed"):
            raise Exception("Connection closed!")
        logger.info(f"What's the error: {e}")

    logger.info(f"Prices Updated {current_time}")
