import json
from services.config import config_service
from services import database_service


def create_event_create_claim_mutation(hash, event_type,
                                       events_arr, height, timestamp, recipient_addr,
                                       sender_addr, amount, token, claim_type, module, prophecy_status):

    if amount is None:
        sql_str = '''
        INSERT INTO {10}
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, claim_type, module, prophecy_status,
                   config_service.schema_config['EVENTS_TABLE_V2'])
    else:
        sql_str = '''
        INSERT INTO {12}
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_amount, cc_token, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, claim_type, module, prophecy_status,
                   config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
