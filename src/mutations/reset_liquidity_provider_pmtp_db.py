from services import database_service


def reset_liquidity_provider_pmtp_db_mutation():
    sql_str = """
    truncate table pmtp_liquidity_provider_process
    """
    database_service.execute_update(sql_str)
