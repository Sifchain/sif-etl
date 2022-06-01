import json
from services.config import config_service
from services import database_service


def create_event_remove_liquidity_mutation(hash, event_type,
                                           events_arr, height, timestamp, rl_token, rl_provider, rl_amount, rl_token2, rl_amount2, pool):

    if rl_amount2 is None:
        sql_str = '''
            INSERT INTO {9}
            (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_pool)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
            '''.format(hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                       rl_provider, rl_amount, pool,
                       config_service.schema_config['EVENTS_TABLE_V2'])
    else:
        sql_str = '''
        INSERT INTO {11}
        (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_token2, rl_amount2, 
        rl_pool)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                   rl_provider, rl_amount,
                   rl_token2, rl_amount2, pool, config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
