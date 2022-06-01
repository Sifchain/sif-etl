import json
from services.config import config_service
from services import database_service


def create_event_unknown_mutation(hash, event_type, events,
                                  height, timestamp):
    sql_str = """
    INSERT INTO {6}
    (hash, type, log, height, time, description)
     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
    """.format(hash, event_type, json.dumps(events), height, timestamp, 'UNKNOWN', config_service.schema_config["EVENTS_TABLE_V2"])

    database_service.execute_update(sql_str)
