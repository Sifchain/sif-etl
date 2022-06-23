import json

from src.services.database import database_service


def create_event_edit_validator_mutation(hash, event_type,
                                         events_arr, height, timestamp,
                                         sender, min_self_delegation, commission_rate, max_commission_change_rate, max_commission_rate, gasWanted, gasUsed):

    sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        ev_sender,
        ev_min_self_delegation, ev_commission_rate, ev_max_commission_change_rate,
        ev_max_commission_rate,
        ev_gas_wanted, ev_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' ,'{10}', '{11}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   sender, min_self_delegation, commission_rate, max_commission_change_rate,
                   max_commission_rate, gasWanted, gasUsed)

    database_service.execute_update(sql_str)
