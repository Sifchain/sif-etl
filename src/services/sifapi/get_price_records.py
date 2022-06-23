import requests
import logging

from src.queries.get_token_decimal_dictionary_db import get_token_decimal_dictionary_db_query
from src.services.config import config_service
from src.services.sifapi.get_timestamp_from_height import get_timestamp_from_height_sifapi
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("get_price_records_pmtp_sifapi", formatter)

LCD_SERVER_URL = config_service.api_config["LCD_SERVER_URL"]


def get_price_records_sifapi():
    token_registry = get_token_decimal_dictionary_db_query()
    token_decimals_dictionary = {}
    for token in token_registry:
        token_decimals_dictionary[token["hash_symbol"].lower()] = (
            token["decimals"],
            token["symbol"],
        )

    json_data = requests.get("{0}/clp/getPools".format(LCD_SERVER_URL)).json()
    height = json_data["height"]
    pools = json_data["result"]["pools"]

    timestamp = get_timestamp_from_height_sifapi(height)
    rowan_cusdt = None

    # Get the conversion rate for rowan/cusdt

    for pool in pools:
        if pool["external_asset"]["symbol"] == "cusdt":
            # rowan as 18 decimals
            rowan_units = float(pool["native_asset_balance"]) / 10 ** 18
            # cusdt has 6 decimals
            cusdt_units = float(pool["external_asset_balance"]) / 10 ** 6
            rowan_cusdt = cusdt_units / rowan_units
            break

    if rowan_cusdt is None:
        raise Exception(f"Rowan is not initialized: {rowan_cusdt} at {height}")

    token_prices_dict = {"rowan_cusdt": rowan_cusdt}

    for pool in pools:
        # total rowans in this pool divided by rowan decimals
        rowan_units = float(pool["native_asset_balance"]) / 10 ** 18

        external_asset_symbol = pool["external_asset"]["symbol"].lower()
        external_asset_decimals = token_decimals_dictionary[external_asset_symbol][0]
        external_asset_symbol = token_decimals_dictionary[external_asset_symbol][1]

        # total tokens in this pool divided by its decimals
        external_asset_units = (
            float(pool["external_asset_balance"]) /
            10 ** external_asset_decimals
        )

        token_prices_dict[external_asset_symbol + "_rowan"] = float(
            rowan_units / external_asset_units
        )
        token_prices_dict[external_asset_symbol + "_cusdt"] = float(
            rowan_units / external_asset_units * rowan_cusdt
        )

    return (token_prices_dict, rowan_cusdt, height, timestamp)
