import json

from src.services.database import database_service


def create_event_redelegate_mutation(hash, event_type,
                                     events_arr, height, timestamp, source_validator, destination_validator, recipient_addr,
                                     sender_addr, token, amount, gasWanted, gasUsed):

    sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        re_recipient_addr,
        re_sender_addr, re_amount, re_token, re_gas_wanted, re_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, gasWanted, gasUsed)

    database_service.execute_update(sql_str)
