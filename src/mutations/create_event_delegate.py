import json
from services.config import config_service
from services import database_service


def create_event_delegate_mutation(hash, event_type,
                                   events_arr, height, timestamp, validator_addr,
                                   sender_addr, amount, gasWanted, gasUsed):

    sql_str = '''
        INSERT INTO {10}
        (hash, type, log, height, time, 
        de_validator_addr,
        de_sender_addr, de_amount, de_gas_wanted, de_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator_addr, sender_addr, amount, gasWanted, gasUsed,
                   config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
