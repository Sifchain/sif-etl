import requests
import os
import logging
from services.config import config_service
from services.sifapi.get_timestamp_from_height_pmtp import get_timestamp_from_height_pmtp_sifapi
from queries.get_token_decimal_dictionary_db import get_token_decimal_dictionary_db_query
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("get_price_records_pmtp_sifapi", formatter)

LCD_SERVER_PMTP = os.getenv("LCD_SERVER_PMTP")


def get_price_records_pmtp_sifapi():
    token_registry = get_token_decimal_dictionary_db_query()
    token_decimals_dictionary = {}
    for token in token_registry:
        token_decimals_dictionary[token["hash_symbol"].lower()] = (
            token["decimals"],
            token["symbol"],
        )

    json_data = requests.get(f"{LCD_SERVER_PMTP}/clp/getPools").json()
    height = json_data["height"]

    pools = json_data["result"]["pools"]

    timestamp = get_timestamp_from_height_pmtp_sifapi(height)
    rowan_cusdt = None

    # Get the conversion rate for rowan/cusdt
    for pool in pools:
        if pool["external_asset"]["symbol"] == "cusdt":
            # rowan as 18 decimals
            rowan_cusdt = float(pool["swap_price_native"])
            break

    if rowan_cusdt is None:
        raise Exception(f"Rowan is not initialized: {rowan_cusdt} at {height}")

    token_prices_dict = {"rowan_cusdt": rowan_cusdt}

    for pool in pools:
        # total rowans in this pool divided by rowan decimals

        try:
            external_asset_symbol = pool["external_asset"]["symbol"].lower()

            # total tokens in this pool divided by its decimals
            external_asset_symbol = token_decimals_dictionary[external_asset_symbol][1]

            token_prices_dict[external_asset_symbol + "_rowan"] = float(
                pool["swap_price_native"]
            )
            token_prices_dict[external_asset_symbol + "_reward_distributed"] = float(
                pool["reward_period_native_distributed"]
            )
            token_prices_dict[external_asset_symbol + "_cusdt"] = (
                float(pool["swap_price_external"]) * rowan_cusdt
            )
        except Exception as e:
            logger.info(f"couldn't resolve {e}")

    return (token_prices_dict, rowan_cusdt, height, timestamp)
