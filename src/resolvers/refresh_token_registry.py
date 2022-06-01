from datetime import datetime, timezone
import logging
from services.sifapi import latest_token_registry_sifapi
from mutations import update_token_registry_db_mutation
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("refresh_token_registry_resolver", formatter)


def refresh_token_registry_resolver():
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
