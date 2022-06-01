from queries import get_claims_heights_query
from mutations import add_event_record_mutation


def claims_record_resolver():
    heights = get_claims_heights_query()
    for height in heights:
        add_event_record_mutation(height)
