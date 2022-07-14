import json
import logging
from time import time

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util


def create_price_record_mutation(height, timestamp, rowan_cusdt, token_prices_dict, token_volumes_dict):
    sql_str = """
            insert into prices(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr)
            values ({0}, '{1}', {2}, '{3}', '{4}')
            """.format(height, timestamp, rowan_cusdt, json.dumps(token_prices_dict), json.dumps(token_volumes_dict))
    database_service.execute_update(sql_str)

    sql_str = """
        insert into tokenprices(height, asset_price, asset, time)
        select t.height, cast(p.token_prices->>t.tok as float) as asset_price, t.tok as asset, t.timestamp from       	
        (    
            select height, id, timestamp, json_object_keys(token_prices) as tok
            from prices where height = '{0}'
        ) t
        inner join
        (
            select height, token_prices 
            from prices p 
            where height = '{0}'
        ) p
        on t.height = p.height;
        
        insert into tokenvolumes(height, asset_volume_daily, asset, time)
        select p.height, cast(p.token_volumes_24hr ->> f.tok as numeric) as asset_volume_daily , f.tok as asset, 
        p.timestamp 
        from (
            select height, id, timestamp, json_object_keys(token_volumes_24hr) as tok 
            from prices where height = '{0}'
        ) f 
        inner join (
            select p.* 
            from prices p 
            where height='{0}'
        ) p on f.height = p.height
        """.format(height)
    database_service.execute_update(sql_str)

    sql_str = """
            insert into prices_latest (height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr)
            values ({0}, '{1}', {2}, '{3}', '{4}');

            delete from prices_latest where height < '{0}';
            """.format(height, timestamp, rowan_cusdt, json.dumps(token_prices_dict), json.dumps(token_volumes_dict))
    database_service.execute_update(sql_str)


def create_price_record_pmtp_mutation(height, timestamp, rowan_cusdt, token_prices_dict, token_volumes_dict):
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
    logger = setup_logger_util("create_price_record_pmtp_mutation", formatter)
    logger.info(f"Price updating ...")
    t0 = time()

    sql_str = f'''
            insert into prices(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr) 
            values ({height}, '{timestamp}', {rowan_cusdt}, '{json.dumps(token_prices_dict)}', 
            '{json.dumps(token_volumes_dict)}') 
            '''
    database_service.execute_update(sql_str)

    sql_str = """
    insert into tokenprices(time, asset_price, asset, height, reward_distributed)
    with cte_not_reward as (
        select t.height, cast(p.token_prices->>t.tok as float) as asset_price, t.tok as asset, t.timestamp 
        from 
        (
            select height, id, timestamp, json_object_keys(token_prices) as tok
            from prices 
            where height = '{0}'
        ) t
        inner join 
        (
            select height, token_prices 
            from prices p 
            where height = '{0}'
        ) p
        on t.height = p.height
        where t.tok not like '%reward_distributed'
    ), cte_reward as (
        select t.height, cast(p.token_prices->>t.tok as float) as reward, left(t.tok, length(t.tok)-19) as asset, 
        t.timestamp 
        from (
            select height, id, timestamp, json_object_keys(token_prices) as tok
            from prices 
            where height = '{0}'
        ) t
        inner join 
        (
            select height, token_prices 
            from prices p 
            where height = '{0}'
        ) p
        on t.height = p.height
        where t.tok like '%reward_distributed'
    ),cte_final as (
        select p.timestamp, p.asset_price, p.asset, p.height, a.reward 
        from cte_not_reward p
        left join cte_reward a on a.height = p.height 
        and (a.asset ||'_cusdt' = p.asset or a.asset ||'_rowan' = p.asset)
    )
    select timestamp, asset_price, asset, height, reward  from cte_final
        """.format(height)

    database_service.execute_update(sql_str)

    sql_str = """
        insert into TokenVolumes(height, asset_volume_daily, asset, time)  
        select p.height, cast(p.token_volumes_24hr ->> f.tok as numeric) as asset_volume_daily , f.tok as asset, 
            p.timestamp  
        from (
            select height, id, timestamp, json_object_keys(token_volumes_24hr) as tok 
            from prices 
            where height = '{0}'
        ) f 
        inner join(
            select p.* 
            from prices p 
            where height='{0}'
        ) p on f.height = p.height
        """.format(height)
    database_service.execute_update(sql_str)

    sql_str = """
            insert into prices_latest(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr)
            values ({0}, '{1}', {2}, '{3}', '{4}');

            delete from prices_latest where height < '{0}';
            """.format(height, timestamp, rowan_cusdt,
                       json.dumps(token_prices_dict), json.dumps(token_volumes_dict))
    database_service.execute_update(sql_str)

    sql_str = f"""
            truncate table trade_daily_temp
            """

    database_service.execute_update(sql_str)

    sql_str = f"""
            insert into trade_daily_temp(trading_pairs, highest_price_24h, lowest_price_24h, last_price, opening,
                price_change_percent_24h, base_currency, target_currency, base_volume, target_volume, bid, ask)
            select asset as trading_pairs, high as highest_price_24h, low as lowest_price_24h, last as last_price,
                opening, cast(((last - opening)/p.opening)*100 as float) as price_change_percent_24h,
                left(p.asset::text, length(p.asset::text) - 6) AS base_currency,
                'rowan'::text AS target_currency, coalesce(base_volume, 0) as base_volume,
                coalesce(base_volume/r.rowan_price,0) as target_volume,
                p.last - p.last * 0.002::double precision AS bid,
                p.last AS ask
            from (
                select max(tokenprices."time") AS daily, tokenprices.asset,
                    first(1/tokenprices.asset_price, tokenprices."time") AS opening,
                    max(1/tokenprices.asset_price) AS high, min(1/tokenprices.asset_price) AS low,
                    last(1/tokenprices.asset_price, tokenprices."time") AS last FROM tokenprices
                WHERE tokenprices."time" > (now() - '1 day'::interval)
                and tokenprices.asset_price <> 0.0
                AND tokenprices.asset::text ~~ '%_rowan'::text GROUP BY tokenprices.asset
            ) p
            left join (
                select tok.base_denom as token, base.volume as base_volume
                from (
                    select max(daily) as daily, token, sum(amount) as volume
                    from (
                        select time as daily, ea.swap_begin_token as token, ea.swap_begin_amount as amount
                        from events_audit ea where ea.type = 'swap_successful'
                        and ea.time > (now() - '1 day'::interval)
                        union all
                        select time, ea.swap_final_token token, ea.swap_final_amount
                        from events_audit ea
                        where ea.type = 'swap_successful' and ea.time > (now() - '1 day'::interval) ) f
                        group by token
                    ) base
                    inner join token_registry tok
                    on base.token = lower(tok.denom)
            ) vol on p.asset = (vol.token|| '_rowan')
            inner join (
                select rowan_cusdt as rowan_price
                from prices_latest
            ) r on 1=1
            """

    database_service.execute_update(sql_str)

    sql_str = f"""
        update trade_daily_temp td
        set liquidity_in_usd = pi2.external_asset_bal_usd + pi2.native_asset_bal_usd
        from
        (token_registry tr inner join pmtp_pool_info pi2 on pi2.pool = tr.denom) pi2 where pi2.base_denom = td.base_currency
            """
    database_service.execute_update(sql_str)
    tf = time()
    logger.info(f"Price updated in {tf - t0} seconds")
