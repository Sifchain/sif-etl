from src.services.database import database_service


def reset_liquidity_provider_db_atom_mutation():
    sql_str = """
    truncate table liquidity_provider_process_atom
    """
    database_service.execute_update(sql_str)

    sql_str = """
    truncate table reward_payout_process_atom
    """
    database_service.execute_update(sql_str)
