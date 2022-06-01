import requests
from services.config import config_service

RPC_SERVER_URL = config_service.api_config["RPC_SERVER_URL"]


def get_timestamp_from_height_sifapi(height=1):
    block_url = "{0}/block?height={1}".format(RPC_SERVER_URL, height)
    data = requests.get(block_url).json()
    timestamp = data["result"]["block"]["header"]["time"]
    return timestamp
