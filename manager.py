import sys

from src.commands.event_record_continuous import event_record_continuous_command
from src.commands.latest_run import latest_run_command
from src.mutations.add_event_record import add_event_record_mutation
from src.resolvers.add_cmc_price_continuous import add_cmc_price_continuous_resolver
from src.resolvers.add_pool_record_continuous import add_pool_record_continuous_resolver
from src.resolvers.add_price_record import add_price_record_resolver
from src.resolvers.add_price_record_continuous import (
    add_price_record_continuous_resolver,
)
from src.resolvers.add_price_record_pmtp import add_price_record_pmtp_resolver
from src.resolvers.add_spiked_cache import add_spiked_cache_resolver
from src.resolvers.refresh_token_registry import refresh_token_registry_resolver
from src.resolvers.update_once_day import update_once_day_resolver

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No command has been passed")
    elif sys.argv[1] == "cron":
        latest_run_command()
    elif sys.argv[1] == "tokenregistry":
        refresh_token_registry_resolver()
    elif sys.argv[1] == "external_price":
        add_cmc_price_continuous_resolver()
    elif sys.argv[1] == "add_price_record":
        add_price_record_resolver()
    elif sys.argv[1] == "add_price_record_pmtp":
        add_price_record_pmtp_resolver()
    elif sys.argv[1] == "add_price_record_continuous":
        add_price_record_continuous_resolver()
    elif sys.argv[1] == "refresh_pricespikes":
        add_spiked_cache_resolver()
    elif sys.argv[1] == "update_once_day":
        update_once_day_resolver()
    elif sys.argv[1] == "event_record_continuous":
        event_record_continuous_command()
    else:
        # Test out one event dispensation
        # This is claims snapshot
        add_event_record_mutation(6697419)
