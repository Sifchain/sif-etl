import json
from services.config import config_service
from services import database_service


def create_event_distribution_started_mutation(hash, event_type,
                                               events_arr, height, timestamp,
                                               sender, recipient, action, token, amount, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO {12}
    (hash, type, log, height, time,
    ds_sender, ds_recipient, ds_action,
    ds_token, ds_amount,
    ds_gasWanted, ds_gasUsed)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', 
    '{8}', '{9}', 
    '{10}','{11}'
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, recipient, action,
               token, amount,
               gasWanted, gasUsed,
               config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
