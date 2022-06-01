import json
import logging
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_event_unlock_liquidity_mutation", formatter)


def create_event_unlock_liquidity_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           liquidity_provider, liquidity_units, pool
                                           ):

    sql_str = f'''
    INSERT INTO events_audit
    (hash, type, log, height, time,
    ul_address, ul_unit, ul_pool)
    VALUES ('{hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', 
    '{liquidity_provider}', {liquidity_units}, '{pool}' 
    )
    '''
    logger.info(sql_str)

    database_service.execute_update(sql_str)
