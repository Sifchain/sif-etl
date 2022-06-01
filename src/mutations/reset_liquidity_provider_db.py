from services import database_service


def reset_liquidity_provider_db_mutation():
    sql_str = """
    truncate table liquidity_provider_process
    """
    database_service.execute_update(sql_str)

    sql_str = """
    truncate table reward_payout_process 
    """
    database_service.execute_update(sql_str)
