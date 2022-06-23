import json
import logging
import time

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_price_record_pmtp_mutation", formatter)


def create_price_record_pmtp_mutation(height, timestamp, rowan_cusdt, token_prices_dict, token_volumes_dict):
    t0 = time.time()

    sql_str = f'''
            INSERT INTO prices(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr) 
            VALUES ({height}, '{timestamp}', {rowan_cusdt}, '{json.dumps(token_prices_dict)}', '{json.dumps(token_volumes_dict)}') 
            '''
    database_service.execute_update(sql_str)

    sql_str = f"""
        truncate table TokenPrices_staging
        """
    database_service.execute_update(sql_str)

    sql_str = f"""
        insert into TokenPrices_staging
        (height, asset_price, asset, time) 
        select t.height, cast(p.token_prices->>t.tok as float) as asset_price, t.tok as asset, t.timestamp from 
        (select height, id, timestamp, json_object_keys(token_prices) as tok
        from prices where height = {height}
        ) t
        inner join 
        (select height, token_prices from prices p where height = {height}) p
        on t.height = p.height
        where t.tok not like '%reward_distributed'
        """
    database_service.execute_update(sql_str)

    sql_str = f"""
        update tokenprices_staging p
        set reward_distributed =a.reward
         from (      
         select t.height, cast(p.token_prices->>t.tok as float) as reward, left(t.tok, length(t.tok)-19) as asset, t.timestamp from 
            (select height, id, timestamp, json_object_keys(token_prices) as tok
        from prices where height ={height}
        ) t
        inner join 
        (select height, token_prices from prices p where height = {height}) p
        on t.height = p.height
        where t.tok like '%reward_distributed'
        and t.height={height}
        ) a where a.height = p.height 
        and p.height={height}
        and (a.asset ||'_cusdt' = p.asset or a.asset ||'_rowan' = p.asset)
        """
    database_service.execute_update(sql_str)

    sql_str = """
        insert into tokenprices
        (time, asset_price, asset, height, reward_distributed)
        select time, asset_price, asset, height, reward_distributed
        from tokenprices_staging
        """
    database_service.execute_update(sql_str)

    sql_str = """
        insert into TokenVolumes
        (height, asset_volume_daily, asset, time)  
        select p.height, cast(p.token_volumes_24hr ->> f.tok as numeric) as asset_volume_daily , f.tok as asset, p.timestamp  
        from (
        select height, id, timestamp, json_object_keys(token_volumes_24hr) as tok from prices where height = '{0}') f inner join
        (select p.* from prices p where height='{0}') p on f.height = p.height
        """.format(height)
    database_service.execute_update(sql_str)

    sql_str = """
            INSERT INTO prices_latest(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr) 
            VALUES ({0}, '{1}', {2}, '{3}', '{4}');

            delete from prices_latest
            where height < '{0}';

            """.format(height, timestamp, rowan_cusdt,
                       json.dumps(token_prices_dict), json.dumps(token_volumes_dict))
    database_service.execute_update(sql_str)
    tf = time.time()
    logger.info(f"Price updated in {tf - t0} seconds")
