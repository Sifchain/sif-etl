from src.mutations.create_event_unknown import create_event_unknown_mutation


def process_event_unknown_event(hash, event_type, events, height, timestamp):
    create_event_unknown_mutation(hash, event_type, events, height, timestamp)
