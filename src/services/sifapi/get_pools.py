import requests
from services.config import config_service
from queries.get_token_decimal_dictionary_db import get_token_decimal_dictionary_db_query

LCD_SERVER_URL = config_service.api_config["LCD_SERVER_URL"]


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
