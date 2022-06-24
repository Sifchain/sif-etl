from src.services.database import database_service


def update_token_registry_db_mutation(token, current_time):
    base_denom = token["base_denom"]
    denom = token["denom"]
    decimals = token["decimals"]
    is_active = True  # token["is_whitelisted"]

    sql_str = """
    SELECT 1 from token_registry
    where base_denom = '{0}'
    and denom = '{1}'
    and decimals = '{2}'
    and is_active = '{3}'
    """.format(base_denom, denom, decimals, is_active)

    exists = True
    try:
        database_service.execute_scalar(sql_str)
    except Exception:
        exists = False

    if not exists:
        sql_str = """
        UPDATE token_registry 
        set is_active = false
        where (base_denom = '{0}'
        or denom = '{1}')
        and is_active = true;

        INSERT INTO token_registry
        (base_denom, denom, decimals, modified, is_active)
        VALUES 
        ('{0}', '{1}', '{2}', '{3}', '{4}')
        """.format(token["base_denom"], token["denom"], token["decimals"], current_time, is_active)

        database_service.execute_update(sql_str)
