import json
from services.config import config_service
from services import database_service


def create_event_add_lock_mutation(hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, lk_amount, lk_token, lk_amount2, lk_token2):

    if lk_amount2 is None:
        sql_str = '''
        INSERT INTO {9}
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token 
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token,
                   config_service.schema_config['EVENTS_TABLE_V2'])
    else:
        sql_str = '''
        INSERT INTO {11}
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token,
        lk_amount2, lk_token2)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token,
                   lk_amount2, lk_token2,
                   config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
