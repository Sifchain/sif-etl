import json

from src.services.database import database_service


def create_event_distribution_started_mutation(hash, event_type,
                                               events_arr, height, timestamp,
                                               sender, recipient, action, token, amount, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO events_audit
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
               gasWanted, gasUsed)

    database_service.execute_update(sql_str)
