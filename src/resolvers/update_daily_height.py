import logging
from datetime import datetime, timezone

from src.mutations.create_daily_height import create_daily_height_mutation
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("update_daily_height_resolver", formatter)


def update_daily_height_resolver():
    try:
        create_daily_height_mutation()
        logger.info(f"Daily height updated on {datetime.now(timezone.utc)}")
    except Exception as e:
        errormsg = str(e)
        if errormsg.endswith("closed"):
            raise Exception("Connection closed!")

        logger.info(f"What's the error: {e}")
