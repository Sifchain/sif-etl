from time import sleep
from resolvers.update_daily_height import update_daily_height_resolver


def update_once_day_resolver():
    while (True):
        update_daily_height_resolver()
        sleep(3600*24)
