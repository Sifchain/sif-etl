import json

from src.services.database import database_service


def create_event_swap_mutation(hash, event_type,
                               events_arr, height, timestamp,
                               begin_recipient_swap, begin_sender_swap, begin_amount, begin_amount_token,
                               final_recipient_swap, final_sender_swap, final_amount, final_amount_token,
                               liquidity_fee, price_impact):

    sql_str = '''
    INSERT INTO events_audit
    (hash, type, log, height, time,
    swap_begin_recipient, swap_begin_sender, swap_begin_amount, swap_begin_token,
    swap_final_recipient, swap_final_sender, swap_final_amount, swap_final_token,
    swap_liquidity_fee,
    swap_price_impact)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}', 
    '{9}', '{10}', '{11}', '{12}',
    '{13}', 
    '{14}')
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               begin_recipient_swap, begin_sender_swap, begin_amount, begin_amount_token,
               final_recipient_swap, final_sender_swap, final_amount, final_amount_token,
               liquidity_fee, price_impact)

    database_service.execute_update(sql_str)
