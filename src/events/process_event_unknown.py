from src.mutations.create_events import create_event_unknown_mutation


def process_event_unknown_event(_hash, event_type, events, height, timestamp):
    create_event_unknown_mutation(_hash, event_type, events, height, timestamp)
