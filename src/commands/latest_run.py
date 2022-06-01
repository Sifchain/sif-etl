from bisect import bisect_left
import logging
from queries import get_latest_processed_height_query, get_unprocessed_heights_query
from services.sifapi import get_latest_block_height_sifapi
from utils import setup_logger_util
from mutations import add_event_record_mutation

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("latest_run_command", formatter)


def latest_run_command():
    # Only process from the latest run.
    end = get_latest_block_height_sifapi()
    start = get_latest_processed_height_query()
    unprocessed_heights = get_unprocessed_heights_query(end, start)

    height = start

    while (height <= end):
        i = bisect_left(unprocessed_heights, height)
        if i != len(unprocessed_heights) and unprocessed_heights[i] == height:
            logger.debug(f"Processing {height}")
            add_event_record_mutation(height)
        else:
            logger.debug(f"Skiping {height} already processed.")
        height += 1
