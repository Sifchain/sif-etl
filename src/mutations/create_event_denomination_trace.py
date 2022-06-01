import json
from services.config import config_service
from services import database_service


def create_event_denomination_trace_mutation(hash, event_type,
                                             events_arr, height, timestamp,
                                             sender, receiver, denom, amount, success, packet_src_port,
                                             packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
                                             packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence):

    sql_str = '''
    INSERT INTO {19}
    (hash, type, log, height, time,
    dt_sender, dt_receiver, dt_denom, dt_amount, dt_success, 
    dt_packet_src_port, dt_packet_src_channel, dt_packet_dst_port, dt_packet_dst_channel, dt_packet_channel_ordering,
    dt_packet_connection, dt_packet_timeout_timestamp, dt_packet_timeout_height, dt_packet_sequence)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}', '{9}', 
    '{10}','{11}','{12}','{13}','{14}', 
    '{15}','{16}','{17}','{18}'
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, receiver, denom, amount, success,
               packet_src_port, packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
               packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence,
               config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
