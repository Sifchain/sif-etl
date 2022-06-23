import json

from src.services.database import database_service


def create_event_unknown_mutation(hash, event_type, events,
                                  height, timestamp):
    sql_str = """
    INSERT INTO events_audit
    (hash, type, log, height, time, description)
     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
    """.format(hash, event_type, json.dumps(events), height, timestamp, 'UNKNOWN')

    database_service.execute_update(sql_str)
