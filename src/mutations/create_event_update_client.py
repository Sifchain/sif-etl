import json
from services.config import config_service
from services import database_service


def create_event_update_client_mutation(hash, event_type,
                                        events_arr, height, timestamp,
                                        client_id, client_type, consensus_height, header, module):

    sql_str = '''
        INSERT INTO {10}
        (hash, type, log, height, time, 
        uc_client_id, uc_client_type, uc_consensus_height, uc_header, uc_module)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   client_id, client_type, consensus_height, header, module,
                   config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
