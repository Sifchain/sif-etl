import sys
import logging
from bisect import bisect_left
from time import time
from queue import Queue
from threading import Thread

from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_latest_processed_height import get_latest_processed_height_query
from src.queries.get_unprocessed_heights import get_unprocessed_heights_query
from src.services.sifapi import get_latest_block_height_sifapi
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(message)s")
logger = setup_logger_util("multi.py", formatter)


def multi_run(start, end, unprocessed_height=None):
    height = start
    if unprocessed_height is None:
        last_processed_block_height = get_latest_processed_height_query()
        last_unprocessed_block_height = get_latest_block_height_sifapi()
        unprocessed_height = get_unprocessed_heights_query(last_unprocessed_block_height, last_processed_block_height)
    logger.debug(f"{len(unprocessed_height)} already processed.")

    while height <= end:
        i = bisect_left(unprocessed_height, height)
        if i != len(unprocessed_height) and unprocessed_height[i] == height:
            logger.debug(f"Processing {height}")
            add_event_record_mutation(height)
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
            logger.debug(f"start = {start}, end = {end}, unprocessed_heights={len(unprocessed_heights)}")
            try:
                if self.mode == "reprocess":
                    pass
                    # multi_run_refresh(start, end, processed_heights)
                elif self.mode in ["historical", "latest"]:
                    multi_run(start, end, unprocessed_heights)
                # elif self.mode == "claims":
                #     multi_run_claims(start, end, processed_heights)
                # elif self.mode == "txn_detail":
                #     process_event_txn(processed_heights)
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
    latest_processed_height = 7074426 # get_latest_processed_height_query()
    latest_height = get_latest_block_height_sifapi()
    unprocessed_heights = get_unprocessed_heights_query(latest_height, latest_processed_height)

    num_threads = 10
    num_events_per_thread = (int(latest_height - latest_processed_height) // num_threads + 1)
    _process_events(num_threads,
                    latest_processed_height,
                    num_events_per_thread,
                    "latest",
                    unprocessed_heights,
                    )


def main(mode=""):
    # mode latest, historical, reprocess, txn_detail
    ts = time()
    if mode == "historical":
        pass
    # elif mode == "since":
    #     _process_since(5359241)
    # elif mode == "refresh":
    #     pass
    # _process_already_processed_events_again()
    elif mode == "latest":
        _process_latest_events()
    # elif mode == "txn_detail":
    #     _process_txn_detail()
    # elif mode == "event":
    #     _process_since_event(3263832, sys.argv[2])
    # elif mode == "claims":
    #     _process_claims()
    # elif mode == "claim2":
    #     _process_claims2()
    # elif mode == "claim3":
    #     _process_claims3()
    # elif mode == "claim4":
    #     _process_claims4()

    else:
        raise Exception("Unspecified run mode")

    logger.info("Took %s", time() - ts)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("latest")
    else:
        if sys.argv[1] in (
                "refresh",
                "historical",
                "txn_detail",
                "latest",
                "since",
                "event",
                "claims",
                "claim2",
                "claim3",
                "claim4",
        ):
            main(sys.argv[1])
