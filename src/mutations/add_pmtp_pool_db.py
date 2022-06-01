from services import database_service


def add_pmtp_pool_db_mutation(height):
    sql = f"""
    insert into pmtp_pool
    (height, pool, native_asset_balance, external_asset_balance, asset_balance_in_usd, native_asset_bal_usd, external_asset_bal_usd, native_price_usd)
    select {height}, pool, native_asset_balance, external_asset_balance, asset_balance_in_usd, native_asset_bal_usd, external_asset_bal_usd, native_price_usd
    from pmtp_pool_info 
    where height >= {height}
    """
    database_service.execute_update(sql)
