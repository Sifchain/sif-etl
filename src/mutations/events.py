import json
import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_event_unlock_liquidity_mutation", formatter)


def create_event_unlock_liquidity_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           liquidity_provider, liquidity_units, pool
                                           ):

    sql_str = f'''
    insert into events_audit
    (hash, type, log, height, time,
    ul_address, ul_unit, ul_pool)
    VALUES ('{hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', 
    '{liquidity_provider}', {liquidity_units}, '{pool}' 
    )
    '''
    logger.info(sql_str)

    database_service.execute_update(sql_str)


def create_event_acknowledge_packet_mutation(hash, event_type,
                                             events_arr, height, timestamp,
                                             sender, receiver, denom, amount, success, packet_src_port,
                                             packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
                                             packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence, module):

    sql_str = '''
    insert into events_audit
    (hash, type, log, height, time,
    dt_sender, dt_receiver, dt_denom, dt_amount, ap_success, 
    dt_packet_src_port, dt_packet_src_channel, dt_packet_dst_port, dt_packet_dst_channel, dt_packet_channel_ordering,
    dt_packet_connection, dt_packet_timeout_timestamp, dt_packet_timeout_height, dt_packet_sequence, ap_module)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}', '{9}', 
    '{10}','{11}','{12}','{13}','{14}', 
    '{15}','{16}','{17}','{18}','{19}'
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, receiver, denom, amount, success,
               packet_src_port, packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
               packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence, module,)

    database_service.execute_update(sql_str)


def create_event_add_liquidity_mutation(hash, event_type,
                                        events_arr, height, timestamp, al_token, al_provider, al_amount, al_token2, al_amount2, pool):

    if al_amount2 is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        al_token, al_provider, al_amount, al_pool
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   al_token, al_provider, al_amount, pool)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        al_token, al_provider, al_amount,
        al_token2, al_amount2, al_pool)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}',
        '{8}', '{9}', '{10}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   al_token, al_provider, al_amount,
                   al_token2, al_amount2, pool)

    database_service.execute_update(sql_str)
