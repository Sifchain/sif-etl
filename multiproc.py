import sys
import logging
from bisect import bisect_left
from time import time
from queue import Queue
from threading import Thread

from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_latest_processed_height import *
from src.queries.get_unprocessed_heights import *
from src.resolvers.add_price_record_pmtp import add_price_record_pmtp_resolver
from src.services.sifapi import get_latest_block_height_sifapi
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(message)s")
logger = setup_logger_util("multi.py", formatter)


def multi_run(start, end, unprocessed_height=None, process_type="events"):
    height = start
    if unprocessed_height is None:
        if process_type == "events":
            last_processed_block_height = get_latest_processed_height_query()
            last_unprocessed_block_height = get_latest_block_height_sifapi()
            unprocessed_height = get_unprocessed_heights_query(
                last_unprocessed_block_height, last_processed_block_height
            )
        elif process_type == "prices":
            last_event = get_latest_processed_tokenprices_height_query()
            unprocessed_height = get_unprocessed_tokenprices_heights_query(last_event)

    logger.debug(f"{len(unprocessed_height)} already processed.")

    while height <= end:
        i = bisect_left(unprocessed_height, height)
        if i != len(unprocessed_height) and unprocessed_height[i] == height:
            logger.debug(f"Processing {height}")
            if process_type == "events":
                add_event_record_mutation(height)
            elif process_type == "prices":
                add_price_record_pmtp_resolver(height)
        else:
            logger.debug(f"Skipping {height} already processed")
        height += 1


class IngestWorker(Thread):
    def __init__(self, queue, mode):
        Thread.__init__(self)
        self.mode = mode
        self.queue = queue

    def run(self):
        while True:
            start, end, unprocessed_heights = self.queue.get()
            logger.debug(
                f"start = {start}, end = {end}, unprocessed_heights={len(unprocessed_heights)}"
            )
            try:
                if self.mode in ["historical", "latest"]:
                    multi_run(start, end, unprocessed_heights, "events")
                elif self.mode == "prices":
                    multi_run(start, end, unprocessed_heights, "prices")
                else:
                    raise Exception("run mode not specified")
            finally:
                self.queue.task_done()


def _process_events(num_threads, initial_start, num_events, mode, cached_height):
    queue = Queue()
    logger.info(f"Setting up the Queue - {mode} - {len(cached_height)}")
    for x in range(num_threads):
        worker = IngestWorker(queue, mode)
        worker.daemon = True
        worker.start()
    for x in range(num_threads):
        start = x * num_events + initial_start
        end = start + num_events - 1
        queue.put((start, end, cached_height))
    queue.join()


def _process_latest_events():
    latest_processed_height = get_latest_processed_height_query()
    last_event = get_latest_block_height_sifapi()
    unprocessed_heights = get_unprocessed_heights_query(
        last_event, latest_processed_height
    )

    num_threads = 50
    num_events_per_thread = int(last_event - latest_processed_height) // num_threads + 1
    _process_events(
        num_threads,
        latest_processed_height,
        num_events_per_thread,
        "latest",
        unprocessed_heights,
    )


def _process_prices_historical():
    last_event = get_latest_processed_tokenprices_height_query()
    un_process_block_heights = get_unprocessed_tokenprices_heights_query(last_event)
    # num_threads = int(last_event // num_events_per_thread) + 1
    num_threads = 50
    num_events_per_thread = int(last_event - 6539609) // num_threads + 1
    _process_events(
        num_threads,
        1,
        num_events_per_thread,
        "prices",
        un_process_block_heights,
    )


def _process_historical():
    last_event = get_latest_processed_height_query()
    already_processed_block_heights = get_unprocessed_heights_query(last_event)
    # Assume 100 events per minute per thread
    # Gives 4 hours to process everything
    num_events_per_thread = 100 * 60 * 4
    num_threads = int(last_event // num_events_per_thread) + 1
    _process_events(
        num_threads,
        1,
        num_events_per_thread,
        "historical",
        already_processed_block_heights,
    )


def _process_since_event(start_at, event):
    last_event = get_latest_block_height_sifapi()
    logger.info(f"last_event: {last_event}")
    already_processed_block_heights = get_unprocessed_heights_query(
        last_event, start_at, event
    )
    # Assume 100 events per minute per thread
    # Gives 4 hours to process everything
    num_events_per_thread = 100 * 60 * 4
    num_threads = int(last_event // num_events_per_thread) + 1
    _process_events(
        num_threads,
        1,
        num_events_per_thread,
        "historical",
        already_processed_block_heights,
    )


def main(mode=""):
    # mode latest, historical, since, event
    ts = time()
    if mode == "historical":
        _process_historical()
    elif mode == "since":
        _process_since_event(5359241, "swap_successful")
    elif mode == "latest":
        _process_latest_events()
    elif mode == "event":
        _process_since_event(3263832, sys.argv[2])
    elif mode == "prices":
        _process_prices_historical()
    else:
        raise Exception("Unspecified run mode")
    logger.info("Took %s", time() - ts)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("latest")
    else:
        if sys.argv[1] in ("historical", "latest", "since", "event", "prices"):
            main(sys.argv[1])
