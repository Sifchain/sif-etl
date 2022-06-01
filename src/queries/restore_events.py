from services import database_service


def restore_events_query():
    events_query = """
        select logs from events;
        """
    events = database_service.execute_query(events_query)
    for i in events:
        print(i)
    return events
