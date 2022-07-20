from time import sleep

from src.commands.latest_run import latest_run_command


def event_record_continuous_command(testnet: int = None):
    while True:
        if testnet:
            latest_run_command(1)
        else:
            latest_run_command()
        sleep(10)
