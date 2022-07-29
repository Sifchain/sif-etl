from time import sleep

from src.commands.latest_run import latest_run_command


def event_record_continuous_command(is_lpd: int = None):
    while True:
        if is_lpd:
            latest_run_command(1)
        else:
            latest_run_command()
        sleep(10)
