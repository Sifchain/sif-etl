import json

from src.services.database import database_service


def create_event_lddp_rewards_dist_mutation(height, event_type, time, _hash, events_arr, ld_recipient_addr,
                                            ld_total_amount, ld_amount) -> None:
    sql_str = f"""
    insert into events_audit(height,type,"time",hash,log, ld_recipient_addr,ld_total_amount,ld_amount)
    select {height},'{event_type}',cast('{time}' as timestamp),'{_hash}','{json.dumps(events_arr)}'
    ,'{ld_recipient_addr}',{ld_total_amount},'{ld_amount}'    
    """
    database_service.execute_update(sql_str)


def create_event_unlock_liquidity_mutation(_hash, event_type, events_arr, height, timestamp, liquidity_provider,
                                           liquidity_units, pool) -> None:
    sql_str = f'''
    insert into events_audit(hash, type, log, height, time, ul_address, ul_unit, ul_pool)
    values('{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', 
    '{liquidity_provider}', {liquidity_units}, '{pool}')
    '''
    database_service.execute_update(sql_str)


def create_event_acknowledge_packet_mutation(_hash, event_type, events_arr, height, timestamp, sender, receiver, denom,
                                             amount, success, packet_src_port, packet_src_channel, packet_dst_port,
                                             packet_dst_channel, packet_channel_ordering, packet_connection,
                                             packet_timeout_timestamp, packet_timeout_height, packet_sequence,
                                             module) -> None:
    sql_str = '''
    insert into events_audit(hash, type, log, height, time, dt_sender, dt_receiver, dt_denom, dt_amount, ap_success, 
    dt_packet_src_port, dt_packet_src_channel, dt_packet_dst_port, dt_packet_dst_channel, dt_packet_channel_ordering,
    dt_packet_connection, dt_packet_timeout_timestamp, dt_packet_timeout_height, dt_packet_sequence, ap_module)
    select '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', cast(nullif('{8}','None') as numeric), '{9}', 
    '{10}','{11}','{12}','{13}','{14}', '{15}','{16}','{17}','{18}','{19}'    
    '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, sender, receiver, denom, amount, success,
               packet_src_port, packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
               packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence, module)
    database_service.execute_update(sql_str)


def create_event_add_create_liquidity_mutation(_hash, event_type, events_arr, height, timestamp, al_token, al_provider,
                                               al_amount, al_token2, al_amount2, pool) -> None:
    sql_str = f""" 
    insert into events_audit(hash, type, log, height, time, al_token, al_provider, al_amount, al_token2, 
    al_amount2, al_pool) 
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}',
    '{timestamp}', '{al_token}', '{al_provider}',cast(nullif('{al_amount}','None') as numeric), '{al_token2}', 
    cast(nullif('{al_amount2}','None') as numeric), '{pool}' 
    """
    database_service.execute_update(sql_str)


def create_event_rewards_mutation(_hash, event_type, events_arr, height, timestamp, recipient_addr, sender_addr,
                                  amount, token) -> None:
    sql_str = f"""
    insert into events_audit(hash, type, log, height, time,wr_recipient_addr,wr_sender_addr, wr_amount, wr_token)
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', '{recipient_addr}'
    ,'{sender_addr}', cast(nullif('{amount}','None') as numeric), cast(nullif('{token}','None') as varchar) 
    """
    database_service.execute_update(sql_str)


def create_event_user_claims_mutation(height, _hash, event_type, timestamp, address, claim_type, claim_time,
                                      events, raw_claim_time) -> None:
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
    insert into snapshots_claims_v2(created, address, reward_program, claim_time, distribution_type, is_current, 
    height, claim_time_utc)
    values('{timestamp}', '{address}', '{reward_program}', '{claim_time}', '{claim_type}', true, 
    {height}, '{raw_claim_time}')
    """
    database_service.execute_update(sql_str)

    sql_str = f"""
    insert into events_audit(hash, type, log, height, time, description)
    values('{_hash}', '{event_type}', '{json.dumps(events)}', {height}, '{timestamp}', 'snapshot_claims')
    """
    database_service.execute_update(sql_str)


def create_event_update_client_mutation(_hash, event_type, events_arr, height, timestamp, client_id, client_type,
                                        consensus_height, header, module):
    sql_str = '''
    insert into events_audit(hash, type, log, height, time, uc_client_id, uc_client_type, uc_consensus_height, 
    uc_header, uc_module)
    values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')
    '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, client_id, client_type,
               consensus_height, header, module)
    database_service.execute_update(sql_str)


def create_event_unknown_tx_mutation(_hash, event_type, events_arr, height, timestamp) -> None:
    sql_str = """
    insert into events_audit(hash, type, log, height, time)
    values('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(_hash, event_type, json.dumps(events_arr), height, timestamp)
    database_service.execute_update(sql_str)


def create_event_unknown_mutation(_hash, event_type, events, height, timestamp) -> None:
    sql_str = """
    insert into events_audit(hash, type, log, height, time, description)
    values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
    """.format(_hash, event_type, json.dumps(events), height, timestamp, 'UNKNOWN')
    database_service.execute_update(sql_str)


def create_event_unbond_mutation(_hash, event_type, events_arr, height, timestamp, begin_recipient_unbond,
                                 begin_sender_unbond, begin_amount, begin_amount_token, final_recipient_unbond,
                                 final_sender_unbond, final_amount, final_amount_token) -> None:
    if final_amount is None:
        sql_str = '''
        insert into events_audit(hash, type, log, height, time, ub_begin_recipient, ub_begin_sender, 
        ub_begin_amount, ub_begin_token)
        select '{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}', '{8}'
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, begin_recipient_unbond,
                   begin_sender_unbond, begin_amount, begin_amount_token)
    else:
        sql_str = '''
        insert into events_audit(hash, type, log, height, time,ub_begin_recipient, ub_begin_sender, ub_begin_amount, 
        ub_begin_token,ub_final_recipient, ub_final_sender, ub_final_amount, ub_final_token)
        values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}','{9}', '{10}', '{11}', '{12}'
        )
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                   final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token)

    database_service.execute_update(sql_str)


def create_event_swap_mutation(_hash, event_type, events_arr, height, timestamp, begin_recipient_swap,
                               begin_sender_swap, begin_amount, begin_amount_token, final_recipient_swap,
                               final_sender_swap, final_amount, final_amount_token, liquidity_fee,
                               price_impact) -> None:
    sql_str = '''
    insert into events_audit
    (hash, type, log, height, time,
    swap_begin_recipient, swap_begin_sender, swap_begin_amount, swap_begin_token,
    swap_final_recipient, swap_final_sender, swap_final_amount, swap_final_token,
    swap_liquidity_fee,
    swap_price_impact)
    values('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}', 
    '{9}', '{10}', '{11}', '{12}',
    '{13}', 
    '{14}')
    '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
               begin_recipient_swap, begin_sender_swap, begin_amount, begin_amount_token,
               final_recipient_swap, final_sender_swap, final_amount, final_amount_token,
               liquidity_fee, price_impact)

    database_service.execute_update(sql_str)


def create_event_remove_liquidity_mutation(_hash, event_type, events_arr, height, timestamp, rl_token, rl_provider,
                                           rl_amount, rl_token2, rl_amount2, pool):
    if rl_amount2 is None:
        sql_str = '''
            insert into events_audit
            (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_pool)
            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
            '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                       rl_provider, rl_amount, pool)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, rl_token, rl_provider, rl_amount, rl_token2, rl_amount2, 
        rl_pool)
        values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, rl_token,
                   rl_provider, rl_amount,
                   rl_token2, rl_amount2, pool)

    database_service.execute_update(sql_str)


def create_event_redelegate_mutation(_hash, event_type, events_arr, height, timestamp, source_validator,
                                     destination_validator, recipient_addr, sender_addr, token, amount, gas_wanted,
                                     gas_used):
    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        re_recipient_addr,
        re_sender_addr, re_amount, re_token, re_gas_wanted, re_gas_used)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, amount, token, gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_proposal_vote_mutation(_hash, event_type, events_arr, height, timestamp, sender, vote, gas_wanted,
                                        gas_used):
    sql_str = f"""
    insert into events_audit(hash, type, log, height, time,pv_sender, pv_vote, pv_gasWanted, pv_gasUsed)
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}','{sender}', '{vote}', 
    '{gas_wanted}', '{gas_used}'
    """
    database_service.execute_update(sql_str)


def create_event_proposal_deposit_mutation(_hash, event_type,
                                           events_arr, height, timestamp,
                                           sender, recipient, proposal_type, voting_period_start, token,
                                           amount, gas_wanted, gas_used):
    sql_str = '''
    insert into events_audit
    (hash, type, log, height, time,
    pd_sender, pd_recipient, pd_proposal_type,
    pd_voting_period_start, pd_token, pd_amount,
    pd_gasWanted, pd_gasUsed)
    values('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', 
    '{8}', '{9}', '{10}',
    '{11}','{12}'
    )
    '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, recipient, proposal_type, voting_period_start,
               token, amount, gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_post_distribution_mutation(height, timestamp, distribution_rec, distribution_name):
    sql_str = f"""
    delete from post_distribution_v2
    where height = {height}
    """

    database_service.execute_update(sql_str)
    disp_type = None
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


def create_event_edit_validator_mutation(_hash, event_type, events_arr, height, timestamp, sender, min_self_delegation,
                                         commission_rate, max_commission_change_rate, max_commission_rate, gas_wanted,
                                         gas_used):
    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        ev_sender,
        ev_min_self_delegation, ev_commission_rate, ev_max_commission_change_rate,
        ev_max_commission_rate,
        ev_gas_wanted, ev_gas_used)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' ,'{10}', '{11}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   sender, min_self_delegation, commission_rate, max_commission_change_rate,
                   max_commission_rate, gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_distribution_started_mutation(_hash, event_type, events_arr, height, timestamp, sender, recipient,
                                               action, token, amount, gas_wanted, gas_used):
    sql_str = '''
    insert into events_audit
    (hash, type, log, height, time,
    ds_sender, ds_recipient, ds_action,
    ds_token, ds_amount,
    ds_gasWanted, ds_gasUsed)
    values('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', 
    '{8}', '{9}', 
    '{10}','{11}'
    )
    '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, recipient, action,
               token, amount,
               gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_transaction_mutation(_hash, event_type, events_arr, height, timestamp,
                                      sender, receiver, denom, amount, success, packet_src_port,
                                      packet_src_channel, packet_dst_port, packet_dst_channel,
                                      packet_channel_ordering, packet_connection, packet_timeout_timestamp,
                                      packet_timeout_height, packet_sequence) -> None:
    sql_str = f"""
    insert into events_audit (hash, type, log, height, time, dt_sender, dt_receiver, dt_denom, dt_amount, dt_success, 
    dt_packet_src_port, dt_packet_src_channel, dt_packet_dst_port, dt_packet_dst_channel, dt_packet_channel_ordering,
    dt_packet_connection, dt_packet_timeout_timestamp, dt_packet_timeout_height, dt_packet_sequence)
    select '{_hash}', '{event_type}', '{json.dumps(events_arr)}', '{height}', '{timestamp}', '{sender}', '{receiver}', 
    '{denom}', cast(nullif('{amount}','None') as numeric), cast(nullif('{success}','None') as bool),    
    '{packet_src_port}','{packet_src_channel}','{packet_dst_port}','{packet_dst_channel}','{packet_channel_ordering}', 
    '{packet_connection}',cast(nullif('{packet_timeout_timestamp}','None') as numeric), '{packet_timeout_height}','{packet_sequence}' 
    """
    database_service.execute_update(sql_str)


def create_event_delegate_mutation(_hash, event_type, events_arr, height, timestamp, validator_addr, sender_addr,
                                   amount, gas_wanted, gas_used):
    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        de_validator_addr,
        de_sender_addr, de_amount, de_gas_wanted, de_gas_used)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator_addr, sender_addr, amount, gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_create_validator_mutation(_hash, event_type, events_arr, height, timestamp, validator, sender_addr,
                                           token, amount, gas_wanted, gas_used):
    sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cv_validator_addr,
        cv_sender_addr, cv_amount, cv_token, cv_gas_wanted, cv_gas_used)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   validator, sender_addr, amount, token, gas_wanted, gas_used)

    database_service.execute_update(sql_str)


def create_event_create_claim_mutation(_hash, event_type, events_arr, height, timestamp, recipient_addr, sender_addr,
                                       amount, token, claim_type, module, prophecy_status):
    if amount is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_claim_type, cc_module, cc_prophecy_status)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, claim_type, module, prophecy_status)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        cc_recipient_addr,
        cc_sender_addr, cc_amount, cc_token, cc_claim_type, cc_module, cc_prophecy_status)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp, recipient_addr, sender_addr, amount,
                   token, claim_type, module, prophecy_status)

    database_service.execute_update(sql_str)


def create_event_add_lock_mutation(_hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, lk_amount, lk_token, lk_amount2, lk_token2):
    if lk_amount2 is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token 
        )
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        lk_recipient, lk_sender, lk_amount, 
        lk_token,
        lk_amount2, lk_token2)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, lk_amount, lk_token,
                   lk_amount2, lk_token2)

    database_service.execute_update(sql_str)


def create_event_add_burn_mutation(_hash, event_type,
                                   events_arr, height, timestamp,
                                   recipient_addr, sender_addr, bn_amount, bn_token, bn_amount2, bn_token2):
    if bn_amount2 is None:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token
        )
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', '{8}')
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token)
    else:
        sql_str = '''
        insert into events_audit
        (hash, type, log, height, time, 
        bn_recipient, bn_sender, bn_amount, 
        bn_token,
        bn_amount2, bn_token2)
        values('{0}', '{1}', '{2}', '{3}', '{4}', 
        '{5}', '{6}', '{7}', 
        '{8}', '{9}' , '{10}'
        )
        '''.format(_hash, event_type, json.dumps(events_arr), height, timestamp,
                   recipient_addr, sender_addr, bn_amount, bn_token,
                   bn_amount2, bn_token2)

    database_service.execute_update(sql_str)
