from time import sleep

from src.commands.latest_run import latest_run_command


def event_record_continuous_command():
    while True:
        latest_run_command()
        sleep(60)
