from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_re_processed_heights import get_re_processed_heights_query


def single_run_refresh_resolver():
    cached_height = get_re_processed_heights_query()
    for height in cached_height:
        add_event_record_mutation(height)
