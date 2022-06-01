import json
from services.config import config_service
from services import database_service


def create_event_unknown_tx_mutation(hash, event_type, events_arr, height, timestamp):
    sql_str = """
    INSERT INTO {5}
    (hash, type, log, height, time)
    VALUES
    ('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(hash, event_type, json.dumps(events_arr), height, timestamp, config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
