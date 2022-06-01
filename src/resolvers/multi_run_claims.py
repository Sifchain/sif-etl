import logging
from bisect import bisect_left
from queries import get_unprocessed_heights_query
from resolvers import add_event_record_claims_only_resolver
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("multi_run_claims_resolver", formatter)


def multi_run_claims_resolver(start, end, cached_height=None):
    height = start
    if cached_height is None:
        cached_height = get_unprocessed_heights_query(end)
    logger.debug(f"{len(cached_height)} already processed.")
    while (height <= end):
        i = bisect_left(cached_height, height)
        if i != len(cached_height) and cached_height[i] == height:
            logger.debug(f"Processing {height}")
            add_event_record_claims_only_resolver(height)
        else:
            logger.debug(f"Skipping {height} already processed")
        height += 1
