import requests
from services.config import config_service

RPC_SERVER_URL = config_service.api_config["RPC_SERVER_URL"]


def get_latest_block_height_sifapi():
    json_data = requests.get("{0}/status".format(RPC_SERVER_URL)).json()
    latest_height = int(json_data["result"]
                        ["sync_info"]["latest_block_height"])
    return latest_height
