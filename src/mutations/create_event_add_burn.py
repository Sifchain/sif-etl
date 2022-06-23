import json

from src.services.database import database_service


def create_event_add_burn_mutation(hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, bn_amount, bn_token, bn_amount2, bn_token2):

    if bn_amount2 is None:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token,
        bn_amount2, bn_token2)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token,
                   bn_amount2, bn_token2)

    database_service.execute_update(sql_str)
