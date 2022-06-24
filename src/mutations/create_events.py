import json
import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util


def create_event_unlock_liquidity_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           liquidity_provider, liquidity_units, pool
                                           ):
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("create_event_unlock_liquidity_mutation", formatter)
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
                                             packet_src_channel, packet_dst_port, packet_dst_channel,
                                             packet_channel_ordering, packet_connection, packet_timeout_timestamp,
                                             packet_timeout_height, packet_sequence, module):

    sql_str = '''
    insert into events_audit
    (hash, type, log, height, time,
    dt_sender, dt_receiver, dt_denom, dt_amount, ap_success, 
    dt_packet_src_port, dt_packet_src_channel, dt_packet_dst_port, dt_packet_dst_channel, dt_packet_channel_ordering,
    dt_packet_connection, dt_packet_timeout_timestamp, dt_packet_timeout_height, dt_packet_sequence, ap_module)
    select '{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', cast(nullif('{8}','None') as numeric), '{9}', 
    '{10}','{11}','{12}','{13}','{14}', 
    '{15}','{16}','{17}','{18}','{19}'    
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, receiver, denom, amount, success,
               packet_src_port, packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
               packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence, module,)

    database_service.execute_update(sql_str)


def create_event_add_liquidity_mutation(hash, event_type,
                                        events_arr, height, timestamp, al_token, al_provider, al_amount, al_token2,
                                        al_amount2, pool):

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


def create_event_rewards_mutation(_hash, event_type, events_arr, height, timestamp, recipient_addr, sender_addr,
                                  amount, token) -> None:
    sql_str = f"""
    insert into events_audit(hash, type, log, height, time,wr_recipient_addr,wr_sender_addr, wr_amount, wr_token)
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', '{recipient_addr}'
    ,'{sender_addr}', cast(nullif('{amount}','None') as numeric), cast(nullif('{token}','None') as varchar) 
    """
    database_service.execute_update(sql_str)


def create_event_user_claims_mutation(height, hash, event_type, timestamp,  address, claim_type, claim_time,
                                      events, raw_claim_time):

    sql_str = f"""
    delete from snapshots_claims_v2
    where height = {height}
    and address = '{address}'
    and is_current = true

    """
    database_service.execute_update(sql_str)

    if claim_type == 'DISTRIBUTION_TYPE_AIRDROP':
        claim_type = 'Airdrop'
    elif claim_type == 'DISTRIBUTION_TYPE_LIQUIDITY_MINING':
        claim_type = 'lm'
    elif claim_type == 'DISTRIBUTION_TYPE_VALIDATOR_SUBSIDY':
        claim_type = 'vs'

    reward_program = 'harvest'

    sql_str = f"""
    insert into snapshots_claims_v2
    (created, address, reward_program, claim_time, distribution_type, is_current, height, claim_time_utc)
    values
    ('{timestamp}', '{address}', '{reward_program}', '{claim_time}', '{claim_type}', true, {height}, '{raw_claim_time}')
    """

    database_service.execute_update(sql_str)

    sql_str = f"""
    INSERT INTO events_audit
    (hash, type, log, height, time, description)
     VALUES ('{hash}', '{event_type}', '{json.dumps(events)}', {height}, '{timestamp}', 'snapshot_claims')
    """

    database_service.execute_update(sql_str)


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


def create_event_withdraw_commission_mutation(_hash, event_type, events_arr, height, timestamp, amount) -> None:
    sql_str = f"""
    insert into events_audit(hash, type, log, height, time, wc_amount)
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}'
    ,cast(nullif('{amount}','None') as numeric)
    """
    database_service.execute_update(sql_str)
    

def create_event_unknown_tx_mutation(_hash, event_type, events_arr, height, timestamp) -> None:
    sql_str = """
    INSERT INTO events_audit
    (hash, type, log, height, time)
    VALUES
    ('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(_hash, event_type, json.dumps(events_arr), height, timestamp)

    database_service.execute_update(sql_str)


def create_event_unknown_mutation(hash, event_type, events, height, timestamp):
    sql_str = """
    INSERT INTO events_audit
    (hash, type, log, height, time, description)
     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
    """.format(hash, event_type, json.dumps(events), height, timestamp, 'UNKNOWN')

    database_service.execute_update(sql_str)


def create_event_unbond_mutation(hash, event_type,
                                 events_arr, height, timestamp,
                                 begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                                 final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token):

    if final_amount is None:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time,
        ub_begin_recipient, ub_begin_sender, ub_begin_amount, ub_begin_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time,
        ub_begin_recipient, ub_begin_sender, ub_begin_amount, ub_begin_token,
        ub_final_recipient, ub_final_sender, ub_final_amount, ub_final_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}', 
        '{9}', '{10}', '{11}', '{12}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                   final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token)

    database_service.execute_update(sql_str)


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


def create_event_remove_liquidity_mutation(hash, event_type,
                                           events_arr, height, timestamp, rl_token, rl_provider, rl_amount,
                                           rl_token2, rl_amount2, pool):

    if rl_amount2 is None:
        sql_str = '''
            INSERT INTO events_audit
            (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_pool)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
            '''.format(hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                       rl_provider, rl_amount, pool)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_token2, rl_amount2, 
        rl_pool)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                   rl_provider, rl_amount,
                   rl_token2, rl_amount2, pool)

    database_service.execute_update(sql_str)


def create_event_redelegate_mutation(hash, event_type,
                                     events_arr, height, timestamp, source_validator, destination_validator,
                                     recipient_addr, sender_addr, token, amount, gasWanted, gasUsed):

    sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        re_recipient_addr,
        re_sender_addr, re_amount, re_token, re_gas_wanted, re_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_proposal_vote_mutation(hash, event_type,
                                        events_arr, height, timestamp,
                                        sender, vote, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO events_audit
    (hash, type, log, height, time,
    pv_sender, pv_vote, pv_gasWanted, pv_gasUsed)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}' 
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, vote, gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_proposal_deposit_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           sender, recipient, proposal_type, voting_period_start, token,
                                           amount, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO events_audit
    (hash, type, log, height, time,
    pd_sender, pd_recipient, pd_proposal_type,
    pd_voting_period_start, pd_token, pd_amount,
    pd_gasWanted, pd_gasUsed)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', 
    '{8}', '{9}', '{10}',
    '{11}','{12}'
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, recipient, proposal_type, voting_period_start,
               token, amount, gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_post_distribution_mutation(height, timestamp, distribution_rec, distribution_name):

    sql_str = f"""
    delete from post_distribution_v2
    where height = {height}
    """

    database_service.execute_update(sql_str)
    for record in distribution_rec:
        if record['disp_type'] == 'DISTRIBUTION_TYPE_AIRDROP':
            disp_type = 'Airdrop'
        elif record['disp_type'] == 'DISTRIBUTION_TYPE_LIQUIDITY_MINING':
            disp_type = 'LiquidityMining'
        elif record['disp_type'] == 'DISTRIBUTION_TYPE_VALIDATOR_SUBSIDY':
            disp_type = 'ValidatorSubsidy'

        sql_str = f"""
        insert into post_distribution_v2
        (timestamp, height, recipient, amount, distribution_name, disp_type, is_current)
        values
        ('{timestamp}', {height}, '{record["recipient"]}', {record["amount"]}, '{distribution_name}', '{disp_type}'
        , true)
        """

        database_service.execute_update(sql_str)


def create_event_edit_validator_mutation(hash, event_type,
                                         events_arr, height, timestamp,
                                         sender, min_self_delegation, commission_rate, max_commission_change_rate,
                                         max_commission_rate, gasWanted, gasUsed):

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


def create_event_distribution_started_mutation(hash, event_type,
                                               events_arr, height, timestamp,
                                               sender, recipient, action, token, amount, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO events_audit
    (hash, type, log, height, time,
    ds_sender, ds_recipient, ds_action,
    ds_token, ds_amount,
    ds_gasWanted, ds_gasUsed)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', 
    '{8}', '{9}', 
    '{10}','{11}'
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, recipient, action,
               token, amount,
               gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_denomination_trace_mutation(hash, event_type,
                                             events_arr, height, timestamp,
                                             sender, receiver, denom, amount, success, packet_src_port,
                                             packet_src_channel, packet_dst_port, packet_dst_channel,
                                             packet_channel_ordering, packet_connection, packet_timeout_timestamp,
                                             packet_timeout_height, packet_sequence):

    sql_str = '''
    INSERT INTO events_audit
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
               packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence)

    database_service.execute_update(sql_str)


def create_event_delegate_mutation(hash, event_type,
                                   events_arr, height, timestamp, validator_addr,
                                   sender_addr, amount, gasWanted, gasUsed):

    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        de_validator_addr,
        de_sender_addr, de_amount, de_gas_wanted, de_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator_addr, sender_addr, amount, gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_create_validator_mutation(hash, event_type,
                                           events_arr, height, timestamp,
                                           validator,
                                           sender_addr, token, amount, gasWanted, gasUsed):

    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cv_validator_addr,
        cv_sender_addr, cv_amount, cv_token, cv_gas_wanted, cv_gas_used)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator, sender_addr, amount, token, gasWanted, gasUsed)

    database_service.execute_update(sql_str)


def create_event_create_claim_mutation(hash, event_type,
                                       events_arr, height, timestamp, recipient_addr,
                                       sender_addr, amount, token, claim_type, module, prophecy_status):

    if amount is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, claim_type, module, prophecy_status)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_amount, cc_token, cc_claim_type, cc_module, cc_prophecy_status)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, claim_type, module, prophecy_status)

    database_service.execute_update(sql_str)


def create_event_add_lock_mutation(hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, lk_amount, lk_token, lk_amount2, lk_token2):

    if lk_amount2 is None:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token 
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token,
        lk_amount2, lk_token2)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token,
                   lk_amount2, lk_token2)

    database_service.execute_update(sql_str)


def create_event_add_burn_mutation(hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, bn_amount, bn_token, bn_amount2, bn_token2):

    if bn_amount2 is None:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token
        )
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token)
    else:
        sql_str = '''
        INSERT INTO events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token,
        bn_amount2, bn_token2)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token,
                   bn_amount2, bn_token2)

    database_service.execute_update(sql_str)
