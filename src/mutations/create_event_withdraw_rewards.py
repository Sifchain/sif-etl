import json

from src.services.database import database_service


def create_event_withdraw_rewards_mutation(hash, event_type,
                                           events_arr, height, timestamp, recipient_addr,
                                           sender_addr, amount, token):

    if amount is None:
        sql_str = """
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        wr_recipient_addr,
        wr_sender_addr)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}')
        """.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr,
                   sender_addr)
    else:
        sql_str = '''
            INSERT INTO events_audit
            (hash, type, log, height, time, 
            wr_recipient_addr,
            wr_sender_addr, wr_amount, wr_token)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
            '{5}', 
            '{6}', '{7}', '{8}')
            '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                       recipient_addr, sender_addr, amount, token)

    database_service.execute_update(sql_str)
