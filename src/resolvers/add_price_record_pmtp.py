import logging
from services.sifapi import get_price_records_pmtp_sifapi
from queries import get_token_volumes_pmtp_query
from mutations import create_price_record_pmtp_mutation
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_price_record_pmtp_resolver", formatter)


def add_price_record_pmtp_resolver():
    try:

        (token_prices_dict, rowan_cusdt, height,
         timestamp) = get_price_records_pmtp_sifapi()
        token_volumes_dict = get_token_volumes_pmtp_query()

        create_price_record_pmtp_mutation(
            height, timestamp, rowan_cusdt, token_prices_dict, token_volumes_dict)
    except Exception as e:

        logger.info(f"What's the error: {e}")
