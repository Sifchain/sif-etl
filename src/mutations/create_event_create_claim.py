import json

from src.services.database import database_service


def create_event_create_claim_mutation(hash, event_type,
                                       events_arr, height, timestamp, recipient_addr,
                                       sender_addr, amount, token, claim_type, module, prophecy_status):

    if amount is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, claim_type, module, prophecy_status)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_amount, cc_token, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, claim_type, module, prophecy_status)

    database_service.execute_update(sql_str)
