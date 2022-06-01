from queries import get_re_processed_heights_query
from mutations import add_event_record_mutation


def single_run_refresh_resolver():
    cached_height = get_re_processed_heights_query()
    for height in cached_height:
        add_event_record_mutation(height)
