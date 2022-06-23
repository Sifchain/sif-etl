import json

from src.services.database import database_service


def create_event_update_client_mutation(hash, event_type,
                                        events_arr, height, timestamp,
                                        client_id, client_type, consensus_height, header, module):

    sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        uc_client_id, uc_client_type, uc_consensus_height, uc_header, uc_module)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   client_id, client_type, consensus_height, header, module)

    database_service.execute_update(sql_str)
