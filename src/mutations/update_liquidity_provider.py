import logging
import time

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util


def update_liquidity_provider_db_mutation():
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("update_liquidity_provider_db_mutation", formatter)
    t0 = time.time()

    sql_str = f"""
        delete from liquidity_provider
        """

    database_service.execute_query(sql_str)

    sql_str = f"""
        insert into liquidity_provider
        (height, pool, liquidity_provider_units, address, total_units, perc_pool)
        select height, pool, liquidity_provider_units, address, total_units, perc_pool 
        from liquidity_provider_process 
        """
    database_service.execute_query(sql_str)

    sql_str = f"""
        update liquidity_provider as lp
        set pool_balance = perc_pool * p.asset_balance_in_usd,
        pool_balance_external = perc_pool * p.external_asset_bal_usd,
        pool_balance_native = perc_pool * p.native_asset_bal_usd / p.native_price_usd,
        network_pool_external = p.external_asset_bal_usd,
        network_pool_native = p.native_asset_bal_usd/ p.native_price_usd
        from pool_info p where lp.pool = p.pool
        """

    database_service.execute_query(sql_str)
    sql_str = f"""
        update liquidity_provider as lp
        set token = tr.base_denom
        from token_registry tr where tr.denom = lp.pool 
        """

    database_service.execute_query(sql_str)
    tf = time.time()
    logger.info(f"liquidity provider updated in {tf-t0} seconds")


def update_liquidity_provider_db_atom_mutation():
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("update_liquidity_provider_db_atom_mutation", formatter)
    t0 = time.time()

    sql_str = f"""
    delete from liquidity_provider_atom
    """

    database_service.execute_query(sql_str)

    sql_str = f"""
    insert into liquidity_provider_atom
(height, pool, liquidity_provider_units, address, total_units, perc_pool)
    select height, pool, liquidity_provider_units, address, total_units, perc_pool 
    from liquidity_provider_process_atom
    """
    database_service.execute_query(sql_str)

    sql_str = f"""
    update liquidity_provider_atom as lp
    set pool_balance = perc_pool * p.asset_balance_in_usd,
    pool_balance_external = perc_pool * p.external_asset_bal_usd,
    pool_balance_native = perc_pool * p.native_asset_bal_usd / p.native_price_usd,
    network_pool_external = p.external_asset_bal_usd,
    network_pool_native = p.native_asset_bal_usd/ p.native_price_usd
    from pool_info_atom p where lp.pool = p.pool
    """

    database_service.execute_query(sql_str)
    sql_str = f"""
    update liquidity_provider_atom as lp
    set token = tr.base_denom
    from token_registry tr where tr.denom = lp.pool 
    """

    database_service.execute_query(sql_str)
    tf = time.time()
    logger.info(f"atom liquidity provider updated in {tf-t0} seconds")
