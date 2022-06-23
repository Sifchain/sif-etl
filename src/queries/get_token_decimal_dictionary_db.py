from src.services.database import database_service


def get_token_decimal_dictionary_db_query():
    sql_str = """
    select base_denom as symbol, denom as hash_symbol, decimals from token_registry 
    where is_active = true
    """
    return database_service.execute_query(sql_str)
