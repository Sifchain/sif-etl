import logging
import time

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util


def add_liquidity_provider_db_mutation(user_pool_data, pool, height,
                                       native_asset_balance, external_asset_balance, pool_units):
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_db_mutation", formatter)
    t0 = time.time()

    for user_data in user_pool_data:
        sql_str = f"""
            insert into liquidity_provider_process
            (height, pool, liquidity_provider_units, address)
            values
            ({height}, '{pool}', {user_data["liquidity_provider_units"]}, '{user_data["liquidity_provider_address"]}')
        """
        database_service.execute_query(sql_str)

    sql_str = f"""
        update liquidity_provider_process
        set total_units = {pool_units},
        perc_pool = liquidity_provider_units / {pool_units}
        where pool = '{pool}'
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    delete from pool_info where pool='{pool}'
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    insert into pool_info
    (height, pool, native_asset_balance, external_asset_balance)
    values
    ({height}, '{pool}', {native_asset_balance}, {external_asset_balance})
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    update pool_info as pr
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
    from pool_info p 
    inner join token_registry tr on p.pool = tr.denom
    inner join (select asset_price, left(asset, length(asset)-6) as asset from 
    tokenprices where height = (select max(height) from tokenprices) and asset not like '%rowan') pr
    on pr.asset = tr.base_denom 
    inner join (select asset_price, left(asset, length(asset)-6) from tokenprices
    where height = (select max(height) from tokenprices)
    and asset = 'rowan_cusdt'
    ) rowan on 1= 1
    ) p where pr.pool = p.pool
    and p.pool = '{pool}'
    """

    database_service.execute_query(sql_str)

    tf = time.time()
    logger.info(f"liquidity provider process updated in {tf - t0} seconds")


def add_liquidity_provider_db_atom_mutation(user_pool_data, pool, height,
                                            native_asset_balance, external_asset_balance, pool_units):
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_db_atom_mutation", formatter)
    t0 = time.time()

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
    tf = time.time()
    logger.info(f"atom liquidity provider process updated in {tf - t0} seconds")


def add_liquidity_provider_db_pmtp_mutation(user_pool_data, pool, height, pool_units):
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("add_liquidity_provider_db_pmtp_mutation", formatter)
    t0 = time.time()

    for user_data in user_pool_data:
        sql_str = f"""
            insert into pmtp_liquidity_provider_process
            (height, pool, liquidity_provider_units, address)
            values
            ({height}, '{pool}', {
                user_data["liquidity_provider_units"]}, '{user_data["liquidity_provider_address"]}')
        """
        database_service.execute_query(sql_str)

    sql_str = f"""
        update pmtp_liquidity_provider_process
        set total_units = {pool_units},
        perc_pool = liquidity_provider_units / {pool_units}
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    delete from pmtp_liquidity_provider where pool='{pool}'
    """

    database_service.execute_query(sql_str)

    sql_str = f"""
    insert into pmtp_liquidity_provider
    (height, pool, liquidity_provider_units, address, total_units, perc_pool)
    select height, pool, liquidity_provider_units, address, total_units, perc_pool 
    from pmtp_liquidity_provider_process where pool = '{pool}'
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    update pmtp_liquidity_provider as lp
    set pool_balance = perc_pool * p.asset_balance_in_usd,
    pool_balance_external = perc_pool * p.external_asset_bal_usd,
    pool_balance_native = perc_pool * p.native_asset_bal_usd / p.native_price_usd,
    network_pool_external = p.external_asset_bal_usd,
    network_pool_native = p.native_asset_bal_usd/ p.native_price_usd
    from pmtp_pool_info p where lp.pool = p.pool
    and p.pool = '{pool}'

    """

    database_service.execute_query(sql_str)
    sql_str = f"""
    update pmtp_liquidity_provider as lp
    set token = tr.base_denom
    from token_registry tr where tr.denom = lp.pool 
    and lp.pool = '{pool}'
    """

    database_service.execute_query(sql_str)
    tf = time.time()
    logger.info(f"liquidity provider updated in {tf-t0} seconds")
