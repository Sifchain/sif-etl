from src.services.database import database_service


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
        ('{timestamp}', {height}, '{record["recipient"]}', {record["amount"]}, '{distribution_name}', '{disp_type}', true)
        """

        database_service.execute_update(sql_str)
