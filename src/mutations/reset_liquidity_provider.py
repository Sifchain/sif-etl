from src.services.database import database_service


def reset_liquidity_provider_db_mutation():
    sql_str = """
    truncate table liquidity_provider_process
    """
    database_service.execute_update(sql_str)

    sql_str = """
    truncate table reward_payout_process 
    """
    database_service.execute_update(sql_str)


def reset_liquidity_provider_db_atom_mutation():
    sql_str = """
    truncate table liquidity_provider_process_atom
    """
    database_service.execute_update(sql_str)

    sql_str = """
    truncate table reward_payout_process_atom
    """
    database_service.execute_update(sql_str)


def reset_liquidity_provider_pmtp_db_mutation():
    sql_str = """
    truncate table pmtp_liquidity_provider_process
    """
    database_service.execute_update(sql_str)
