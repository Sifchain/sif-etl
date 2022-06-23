import json

from src.services.database import database_service


def create_event_unknown_tx_mutation(hash, event_type, events_arr, height, timestamp):
    sql_str = """
    INSERT INTO events_audit
    (hash, type, log, height, time)
    VALUES
    ('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(hash, event_type, json.dumps(events_arr), height, timestamp)

    database_service.execute_update(sql_str)
