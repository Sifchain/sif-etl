from cmath import log
import sys
from commands import latest_run_command, event_record_continuous_command
from resolvers import refresh_token_registry_resolver, add_price_record_resolver, add_price_record_pmtp_resolver, add_price_record_continuous_resolver, add_spiked_cache_resolver, update_once_day_resolver, add_pool_record_continuous_resolver, add_cmc_price_continuous_resolver
from mutations import add_event_record_mutation

if __name__ == '__main__':
    #### NO COMMAND USED ####
    if len(sys.argv) <= 1:
        print("No command has been passed")

    #### RELATED TO AIRDROPS #####
    elif sys.argv[1] == 'cron':
        latest_run_command()

    #### TOKEN/PRICE UPDATES #####
    elif sys.argv[1] == 'tokenregistry':
        refresh_token_registry_resolver()
    elif sys.argv[1] == 'external_price':
        add_cmc_price_continuous_resolver()
    elif sys.argv[1] == 'add_price_record':
        add_price_record_resolver()
    elif sys.argv[1] == 'add_price_record_pmtp':
        add_price_record_pmtp_resolver()

    elif sys.argv[1] == 'add_price_record_continuous':
        add_price_record_continuous_resolver()
    elif sys.argv[1] == 'refresh_pricespikes':
        add_spiked_cache_resolver()

    elif sys.argv[1] == 'update_once_day':
        update_once_day_resolver()
    elif sys.argv[1] == 'add_pool_record_continuous':
        add_pool_record_continuous_resolver()

    ##### EVENTS_AUDIT UPDATES #####
    elif sys.argv[1] == 'event_record_continuous':
        event_record_continuous_command()

    else:
        # Test out one event dispensation
        # This is claims snapshot
        add_event_record_mutation(6697419)
