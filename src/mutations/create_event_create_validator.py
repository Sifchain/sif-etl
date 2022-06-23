import json

from src.services.database import database_service


def create_event_create_validator_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           validator,
                                           sender_addr, token, amount, gasWanted, gasUsed):

    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cv_validator_addr,
        cv_sender_addr, cv_amount, cv_token, cv_gas_wanted, cv_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator, sender_addr, amount, token, gasWanted, gasUsed)

    database_service.execute_update(sql_str)
