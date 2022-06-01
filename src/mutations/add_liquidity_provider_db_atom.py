import time
import logging
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "add_liquidity_provider_db_atom_mutation", formatter)


def add_liquidity_provider_db_atom_mutation(user_pool_data, pool, height,
                                            native_asset_balance, external_asset_balance, pool_units):
    t0 = time()

    for user_data in user_pool_data:
        sql_str = f"""
            insert into liquidity_provider_process_atom
            (height, pool, liquidity_provider_units, address)
            values
            ({height}, '{pool}', {
                user_data["liquidity_provider_units"]}, '{user_data["liquidity_provider_address"]}')
        """
        database_service.execute_query(sql_str)

    sql_str = f"""
        update liquidity_provider_process_atom
        set total_units = {pool_units},
        perc_pool = liquidity_provider_units / {pool_units}
        where pool = '{pool}'
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    delete from pool_info_atom where pool='{pool}'
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    insert into pool_info_atom
    (height, pool, native_asset_balance, external_asset_balance)
    values
    ({height}, '{pool}', {native_asset_balance}, {external_asset_balance})
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
            update pool_info_atom as pr
    set native_asset_bal_usd = p.native_asset_balance,
    external_asset_bal_usd = p.external_asset_balance,
    native_price_usd = p.native_price_usd,
    external_price_usd = p.external_price_usd,
    asset_balance_in_usd = p.native_asset_balance + p.external_asset_balance
    from (
    select p.pool, native_asset_balance* rowan.asset_price/1e18 as native_asset_balance,  
    external_asset_balance/power(10,tr.decimals)*pr.asset_price as external_asset_balance,
    pr.asset_price as external_price_usd,
    rowan.asset_price as native_price_usd
    from pool_info_atom p 
    inner join token_registry tr on p.pool = tr.denom
    inner join (select asset_price, left(asset, length(asset)-6) as asset from 
    tokenprices where height = (select max(height) from tokenprices where height < {height}) and asset not like '%rowan') pr
    on pr.asset = tr.base_denom 
    inner join (select asset_price, left(asset, length(asset)-6) from tokenprices
    where height = (select max(height) from tokenprices where height <{height})
    and asset = 'rowan_cusdt'
    ) rowan on 1= 1
    ) p where pr.pool = p.pool

    """

    database_service.execute_query(sql_str)

    tf = time()

    logger.info(f"atom liquidity provider process updated in {tf-t0} seconds")
