import requests

from src.services.config import config_service


def latest_token_registry_sifapi():
    token_list_url = config_service.api_config["TOKEN_LIST"]
    token_list = requests.get(token_list_url).json()[
        "result"]["registry"]["entries"]

    return token_list
