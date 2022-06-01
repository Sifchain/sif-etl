import requests
import time
import logging
import os
from services import config_service
from utils import setup_logger_util
from mutations import reset_liquidity_provider_pmtp_db_mutation, add_pool_info_db_pmtp_mutation, add_pmtp_pool_db_mutation

LCD_SERVER_PMTP = os.getenv("LCD_SERVER_PMTP")

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_liquidity_provider_atom_resolver", formatter)


def add_liquidity_provider_pmtp_resolver():

    url = f"{LCD_SERVER_PMTP}/clp/getPools"

    json_data = requests.get(url).json()
    token_list = json_data["result"]["pools"]
    height = json_data["height"]

    t0 = time()

    reset_liquidity_provider_pmtp_db_mutation()

    for token in token_list:
        #        tt0=time()
        logger.info(f"Processing - {token['external_asset']['symbol']}")
        try:
            token_symbol = token['external_asset']['symbol']
            native_asset_balance = token["native_asset_balance"]
            external_asset_balance = token["external_asset_balance"]
        #    pool_units = token["pool_units"]
        #    offset = 0
        #    user_data_token = []

            add_pool_info_db_pmtp_mutation(token_symbol, height,
                                           native_asset_balance, external_asset_balance)
            """

            while True: 
                try:
                    url = f"{LCD_SERVER_PMTP}/clp/getLpList?symbol={token_symbol}&offset={offset}&limit=200"
                    json_data = requests.get(url).json()
                    height = json_data["height"]
                    user_data = json_data["result"]
                    if user_data is None:
                        break 
                    user_data_token = user_data_token + user_data
                    offset +=len(user_data)
                except Exception as e:
                    logger.info(f"Error encountered while looping on {token_symbol} at {offset}")
            ttf=time()
            logger.info(f"Retrieved {token_symbol} in {ttf-tt0} seconds")
            if len(user_data_token) > 0:
                add_liquidity_provider_db_pmtp(user_data_token, token_symbol, height, pool_units)
                """
        except Exception as e:
            logger.info(
                f"Error on {token['external_asset']['symbol']} - Skipping: {e}")

    tf = time()
    add_pmtp_pool_db_mutation(height)
    logger.info(f"Total Tokens processed in {tf-t0} seconds.")
