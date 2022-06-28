import requests
import time

from src.mutations.add_liquidity_provider import *
from src.mutations.add_pmtp_pool_db import add_pmtp_pool_db_mutation
from src.mutations.add_pool_info_db_pmtp import add_pool_info_db_pmtp_mutation
from src.mutations.reset_liquidity_provider import *
from src.mutations.update_liquidity_provider import *
from src.services.config import config_service
from src.utils.setup_logger import setup_logger_util

LCD_SERVER_URL = config_service.api_config["LCD_SERVER_URL"]
LCD_SERVER_PMTP = config_service.api_config["LCD_SERVER_PMTP"]


def add_liquidity_provider_resolver():
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_atom_resolver", formatter)
    url = f"{LCD_SERVER_URL}/clp/getPools"

    json_data = requests.get(url).json()
    token_list = json_data["result"]["pools"]

    t0 = time.time()
    reset_liquidity_provider_db_mutation()
    for token in token_list:
        tt0 = time.time()
        logger.info(f"Processing - {token['external_asset']['symbol']}")
        try:
            token_symbol = token['external_asset']['symbol']
            native_asset_balance = token["native_asset_balance"]
            external_asset_balance = token["external_asset_balance"]
            pool_units = token["pool_units"]
            offset = 0
            user_data_token = []

            while True:
                try:
                    url = f"{LCD_SERVER_URL}/clp/getLpList?symbol={token_symbol}&offset={offset}&limit=200&"
                    json_data = requests.get(url).json()
                    height = json_data["height"]
                    user_data = json_data["result"]
                    if user_data is None:
                        break
                    user_data_token = user_data_token + user_data
                    offset += len(user_data)
                except Exception as e:
                    logger.info(
                        f"Error encountered while looping on {token_symbol} at {offset}")
            ttf = time.time()
            logger.info(f"Retrieved {token_symbol} in {ttf-tt0} seconds")
            if len(user_data_token) > 0:
                add_liquidity_provider_db_mutation(
                    user_data_token, token_symbol, height, native_asset_balance, external_asset_balance, pool_units)
        except Exception as e:
            logger.info(
                f"Error on {token['external_asset']['symbol']} - Skipping: {e}")

    update_liquidity_provider_db_mutation()
    tf = time.time()
    logger.info(f"Total Tokens processed in {tf-t0} seconds.")


def add_liquidity_provider_atom_resolver():
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_atom_resolver", formatter)
    gheight = 6923015
    url = f"https://sifchain.fasthub.io/api/clp/getPools?height={gheight}"

    json_data = requests.get(url).json()
    token_list = json_data["result"]["pools"]
    t0 = time.time()
    reset_liquidity_provider_db_atom_mutation()
    for token in token_list:
        tt0 = time.time()
        logger.info(f"Processing - {token['external_asset']['symbol']}")
        try:
            token_symbol = token['external_asset']['symbol']
            native_asset_balance = token["native_asset_balance"]
            external_asset_balance = token["external_asset_balance"]
            pool_units = token["pool_units"]
            offset = 0
            user_data_token = []

            while True:
                try:
                    url = f"https://sifchain.fasthub.io/api/clp/getLpList?symbol={token_symbol}&offset={offset}&limit=200&height={gheight}"
                    json_data = requests.get(url).json()
                    height = json_data["height"]
                    user_data = json_data["result"]
                    if user_data is None:
                        break
                    user_data_token = user_data_token + user_data
                    offset += len(user_data)
                except Exception as e:
                    logger.info(
                        f"Error encountered while looping on {token_symbol} at {offset}")
            ttf = time.time()
            logger.info(f"Retrieved {token_symbol} in {ttf-tt0} seconds")
            if len(user_data_token) > 0:
                add_liquidity_provider_db_atom_mutation(
                    user_data_token, token_symbol, height, native_asset_balance, external_asset_balance, pool_units)
        except Exception as e:
            logger.info(
                f"Error on {token['external_asset']['symbol']} - Skipping: {e}")

    update_liquidity_provider_db_atom_mutation()
    tf = time.time()
    logger.info(f"Total Tokens processed in {tf-t0} seconds.")


def add_liquidity_provider_pmtp_resolver():
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_atom_resolver", formatter)
    url = f"{LCD_SERVER_PMTP}/clp/getPools"

    json_data = requests.get(url).json()
    token_list = json_data["result"]["pools"]
    height = json_data["height"]

    t0 = time.time()

    # reset_liquidity_provider_pmtp_db_mutation()

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

        except Exception as e:
            logger.info(
                f"Error on {token['external_asset']['symbol']} - Skipping: {e}")

    tf = time.time()
    add_pmtp_pool_db_mutation(height)
    logger.info(f"Total Tokens processed in {tf-t0} seconds.")
