import json

from src.services.database import database_service


def create_event_delegate_mutation(hash, event_type,
                                   events_arr, height, timestamp, validator_addr,
                                   sender_addr, amount, gasWanted, gasUsed):

    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        de_validator_addr,
        de_sender_addr, de_amount, de_gas_wanted, de_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator_addr, sender_addr, amount, gasWanted, gasUsed)

    database_service.execute_update(sql_str)
