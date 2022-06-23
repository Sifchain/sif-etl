from src.mutations.add_event_record import add_event_record_mutation
from src.queries.get_claims_heights import get_claims_heights_query


def claims_record_resolver():
    heights = get_claims_heights_query()
    for height in heights:
        add_event_record_mutation(height)
