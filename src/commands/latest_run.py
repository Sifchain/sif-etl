from bisect import bisect_left

from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_latest_processed_height import get_latest_processed_height_query
from src.queries.get_unprocessed_heights import get_unprocessed_heights_query
from src.services.sifapi import *
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("latest_run_command", formatter)


def latest_run_command():
    # Only process from the latest run.
    end = get_latest_block_height_sifapi()
    start = get_latest_processed_height_query()
    unprocessed_heights = get_unprocessed_heights_query(end, start)

    height = start

    while height <= end:
        i = bisect_left(unprocessed_heights, height)
        if i != len(unprocessed_heights) and unprocessed_heights[i] == height:
            logger.debug(f"Processing {height}")
            add_event_record_mutation(height)
        else:
            logger.debug(f"Skipping {height} already processed.")
        height += 1
