import json

from src.services.database import database_service


def create_event_unbond_mutation(hash, event_type,
                                 events_arr, height, timestamp,
                                 begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                                 final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token):

    if final_amount is None:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time,
        ub_begin_recipient, ub_begin_sender, ub_begin_amount, ub_begin_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time,
        ub_begin_recipient, ub_begin_sender, ub_begin_amount, ub_begin_token,
        ub_final_recipient, ub_final_sender, ub_final_amount, ub_final_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}', 
        '{9}', '{10}', '{11}', '{12}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                   final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token)

    database_service.execute_update(sql_str)
