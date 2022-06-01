import requests


def get_timestamp_from_height_pmtp_sifapi(height):
    block_url = f"https://rpc.sifchain.finance/block?height={height}"
    data = requests.get(block_url).json()
    timestamp = data["result"]["block"]["header"]["time"]
    return timestamp
