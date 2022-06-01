import requests
import time
import logging
from utils import setup_logger_util
from mutations import reset_liquidity_provider_db_atom_mutation, add_liquidity_provider_db_atom_mutation, update_liquidity_provider_db_atom_mutation

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_liquidity_provider_atom_resolver", formatter)


def add_liquidity_provider_atom_resolver():

    gheight = 6923015
    url = f"https://sifchain.fasthub.io/api/clp/getPools?height={gheight}"

    json_data = requests.get(url).json()
    token_list = json_data["result"]["pools"]

    t0 = time()

    reset_liquidity_provider_db_atom_mutation()
    for token in token_list:
        tt0 = time()
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
            ttf = time()
            logger.info(f"Retrieved {token_symbol} in {ttf-tt0} seconds")
            if len(user_data_token) > 0:
                add_liquidity_provider_db_atom_mutation(
                    user_data_token, token_symbol, height, native_asset_balance, external_asset_balance, pool_units)
        except Exception as e:
            logger.info(
                f"Error on {token['external_asset']['symbol']} - Skipping: {e}")

    update_liquidity_provider_db_atom_mutation()
    tf = time()
    logger.info(f"Total Tokens processed in {tf-t0} seconds.")
