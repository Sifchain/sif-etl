from datetime import datetime, timezone
from time import sleep, time

from src.mutations.update_token_registry_db import update_token_registry_db_mutation
from src.services.sifapi import *
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("refresh_token_registry_resolver", formatter)


def refresh_token_registry_resolver():
    while True:
        token_list = latest_token_registry_sifapi()

        current_time = datetime.now(timezone.utc)
        for token in token_list:
            try:
                if token["base_denom"] == "basecro":
                    token["base_denom"] = "xbasecro"
                update_token_registry_db_mutation(token, current_time)
            except Exception as exc:
                logger.critical(f"Unable to update {token} due to {exc}")

        logger.info(f"Token Updated {current_time}")
        sleep(600)
