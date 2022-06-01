from datetime import datetime
from services.sifapi.get_pools import get_pools_sifapi
from services.config import config_service
import json
import requests
from mutations import create_cmc_price_record_batch_mutation
from utils import setup_logger_util


class CoinMarketCapService:
    def __init__(self) -> None:
        self.logger = setup_logger_util("coinmarketcap.py")

        self.cmcParameters = {"symbol": "",
                              "convert": "USD", "skip_invalid": "true"}

        self.cmcHeaders = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": config_service.api_config["CMC_PRO_API_KEY"],
        }

    def request_json(self, URL, h, p):
        try:
            response = requests.get(URL, headers=h, params=p, timeout=5)
            # print(response.url)
        except requests.exceptions.RequestException as err:
            self.logger.fatal(err)
            self.logger.fatal("try a different url")
            return {"Error": err}

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code != 500:
                self.logger.fatal(err)
                return {"Error": err}
        try:
            json_obj = response.json()
        except ValueError:
            self.logger.fatal("Response content is not valid JSON")
            self.logger.fatal("address may be misspelled")
            return {"Error": "Response content is not valid JSON"}

        return json_obj

    def get_cmc_price(self) -> dict:
        pools = get_pools_sifapi()

        coinmarketcap_assets = ""
        for pool in pools:
            if pool in ("uregen", "xbasecro"):
                continue
            coinmarketcap_assets = coinmarketcap_assets + pool[1:] + ","

        self.cmcParameters["symbol"] = coinmarketcap_assets[:-1]

        url = config_service.api_config["COINMARKETCAP_URL"]
        cmc = self.request_json(url, self.cmcHeaders, self.cmcParameters)
        return cmc

    def get_cmc_price_v2(self) -> dict:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        cmcParameters = {"convert": "USD", "start": 1,
                         "limit": 1000, "volume_24h_min": 1}
        cmc = self.request_json(url, self.cmcHeaders, cmcParameters)

        return cmc

    def add_cmc_database_v2(self):
        cmc = self.get_cmc_price_v2()
        cmcData = json.dumps(cmc["data"])
        return cmcData

    def add_eeuro(self, cmc):
        eeuro = requests.get("https://api.e-money.com/v1/rate/eeur/usd").json()
        data = {}
        data["is_active"] = 1
        data["circulating_supply"] = 0
        data["total_supply"] = 0
        data["last_updated"] = datetime.now()
        data["cmc_rank"] = 10000
        quote = {}
        quote["price"] = eeuro
        quote["volume_24"] = 0
        quote["price_change_1h"] = 0

        quote["volume_24h"] = 0
        quote["percent_change_1h"] = 0
        quote["percent_change_24h"] = 0
        quote["percent_change_7d"] = 0
        quote["percent_change_30d"] = 0
        quote["percent_change_60d"] = 0
        quote["percent_change_90d"] = 0
        quote["market_cap"] = 0

        data["quote"] = {"USD": quote}

        cmc["data"]["EUR"] = [data]

        return cmc

    def add_cmc_database(self):
        cmc = self.get_cmc_price()
        current_time = cmc["status"]["timestamp"]
        cmc = self.add_eeuro(cmc)

        cmcjson = json.dumps(cmc, indent=4, sort_keys=True, default=str)
        # self.logger.info(cmcjson)
        create_cmc_price_record_batch_mutation(current_time, cmc)


coinmarketcap_service = CoinMarketCapService()
