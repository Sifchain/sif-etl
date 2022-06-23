import logging
from bisect import bisect_left

from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_re_processed_heights import get_re_processed_heights_query
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("multi_run_refresh_resolver", formatter)


def multi_run_refresh_resolver(start, end, cached_height=None):
    # this is to refresh existing data to filter out rpc calls.
    if cached_height is None:
        cached_height = get_re_processed_heights_query()
    logger.debug(f"{len(cached_height)} already processed.")
    height = start

    while height <= end:
        i = bisect_left(cached_height, height)
        if i != len(cached_height) and cached_height[i] == height:
            logger.debug(f"reprocess {height} already processed")
            add_event_record_mutation(height)
        else:
            logger.debug(f"skipping {height}")
        height += 1
