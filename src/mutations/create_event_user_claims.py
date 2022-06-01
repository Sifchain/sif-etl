import json
from services.config import config_service
from services import database_service


def create_event_user_claims_mutation(height, hash, event_type, timestamp,  address, claim_type, claim_time, events, raw_claim_time):

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
