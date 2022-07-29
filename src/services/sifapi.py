import logging

import requests

from src.queries.get_token_decimal_dictionary_db import (
    get_token_decimal_dictionary_db_query,
)
from src.services.config import config_service
from src.utils.setup_logger import setup_logger_util

LCD_SERVER_URL = config_service.api_config["LCD_SERVER_URL"]
LCD_SERVER_PMTP = config_service.api_config["LCD_SERVER_PMTP"]
LCD_SERVER_PMTP_HIST = config_service.api_config["LCD_SERVER_PMTP_HIST"]
RPC_SERVER_URL = config_service.api_config["RPC_SERVER_URL"]
RPC_SERVER_LPD_URL = config_service.api_config["RPC_SERVER_LPD_URL"]

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("get_price_records_pmtp_sifapi", formatter)


def get_latest_block_height_sifapi(is_lpd: int = None) -> int:
    url = f"{RPC_SERVER_URL}/status"
    if is_lpd:
        url = f"{RPC_SERVER_LPD_URL}/status"
    json_data = requests.get(url).json()
    latest_height = int(json_data["result"]["sync_info"]["latest_block_height"])
    return latest_height


def get_pools_sifapi():
    url = LCD_SERVER_URL + "clp/getPools"
    r = requests.get(url).json()
    pools = r["result"]["pools"]
    token_list = get_token_decimal_dictionary_db_query()
    pool_data = {}
    for i in pools:
        d = i
        symbol = i["external_asset"]["symbol"]
        for token in token_list:
            if symbol == token["hash_symbol"]:
                symbol = token["symbol"]
                d["decimals"] = token["decimals"]
        pool_data[symbol] = d
    return pool_data


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
                float(pool["external_asset_balance"]) / 10 ** external_asset_decimals
        )

        token_prices_dict[external_asset_symbol + "_rowan"] = float(
            rowan_units / external_asset_units
        )
        token_prices_dict[external_asset_symbol + "_cusdt"] = float(
            rowan_units / external_asset_units * rowan_cusdt
        )

    return token_prices_dict, rowan_cusdt, height, timestamp


def get_price_records_pmtp_sifapi(height: int = None):
    token_registry = get_token_decimal_dictionary_db_query()
    token_decimals_dictionary = {}
    for token in token_registry:
        token_decimals_dictionary[token["hash_symbol"].lower()] = (
            token["decimals"],
            token["symbol"],
        )

    if height is None:
        json_data = requests.get(f"{LCD_SERVER_PMTP}/clp/getPools").json()
        height = json_data["height"]
        timestamp = get_timestamp_from_height_pmtp_sifapi(height)
    else:
        json_data = requests.get(
            f"{LCD_SERVER_PMTP_HIST}/clp/getPools?height={height}"
        ).json()
        timestamp = get_timestamp_from_height_sifapi(height)

    rowan_cusdt = None
    pools = json_data["result"]["pools"]

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

    return token_prices_dict, rowan_cusdt, height, timestamp


def get_timestamp_from_height_sifapi(height=1, testnet: int = None):
    block_url = f"{RPC_SERVER_URL}/block?height={height}"
    if testnet:
        block_url = f"{RPC_SERVER_LPD_URL}/block?height={height}"
    data = requests.get(block_url).json()
    timestamp = data["result"]["block"]["header"]["time"]
    return timestamp


def latest_token_registry_sifapi():
    token_list_url = config_service.api_config["TOKEN_LIST"]
    token_list = requests.get(token_list_url).json()["result"]["registry"]["entries"]
    return token_list


def get_timestamp_from_height_pmtp_sifapi(height):
    block_url = f"https://rpc.sifchain.finance/block?height={height}"
    data = requests.get(block_url).json()
    timestamp = data["result"]["block"]["header"]["time"]
    return timestamp
