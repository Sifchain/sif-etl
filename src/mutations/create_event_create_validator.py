import json
from services.config import config_service
from services import database_service


def create_event_create_validator_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           validator,
                                           sender_addr, token, amount, gasWanted, gasUsed):

    sql_str = '''
        INSERT INTO {11}
        (hash, type, log, height, time, 
        cv_validator_addr,
        cv_sender_addr, cv_amount, cv_token, cv_gas_wanted, cv_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator, sender_addr, amount, token, gasWanted, gasUsed,
                   config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
