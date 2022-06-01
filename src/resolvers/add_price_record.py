import logging
from services.sifapi import get_price_records_sifapi
from queries import get_token_volumes_query
from mutations import create_price_record_mutation
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_price_record_resolver", formatter)


def add_price_record_resolver():
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
