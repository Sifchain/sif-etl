import logging
import time

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "add_liquidity_provider_db_pmtp_mutation", formatter)


def add_liquidity_provider_db_pmtp_mutation(user_pool_data, pool, height,
                                            pool_units):
    t0 = time()

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

    tf = time()

    logger.info(f"liquidity provider updated in {tf-t0} seconds")
