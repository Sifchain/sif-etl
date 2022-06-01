import json
from services.config import config_service
from services import database_service
from utils import setup_logger_util


def create_price_record_mutation(height, timestamp, rowan_cusdt, token_prices_dict, token_volumes_dict):
    sql_str = '''
            INSERT INTO {0}(height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr)
            VALUES ({1}, '{2}', {3}, '{4}', '{5}')
            '''.format(config_service.schema_config['PRICES_TABLE'], height, timestamp, rowan_cusdt,
                       json.dumps(token_prices_dict), json.dumps(token_volumes_dict))

    database_service.execute_update(sql_str)

    sql_str = """
        insert into TokenPrices
    	(height, asset_price, asset, time)
       	select t.height, cast(p.token_prices->>t.tok as float) as asset_price, t.tok as asset, t.timestamp from
        (select height, id, timestamp, json_object_keys(token_prices) as tok
        from prices where height = '{0}'
        ) t
        inner join
        (select height, token_prices from prices p where height = '{0}') p
        on t.height = p.height;

        insert into TokenVolumes
		(height, asset_volume_daily, asset, time)
        select p.height, cast(p.token_volumes_24hr ->> f.tok as numeric) as asset_volume_daily , f.tok as asset, p.timestamp
	    from (
		select height, id, timestamp, json_object_keys(token_volumes_24hr) as tok from prices where height = '{0}') f inner join
		(select p.* from prices p where height='{0}') p on f.height = p.height

        """.format(height)

    database_service.execute_update(sql_str)

    sql_str = """
            INSERT INTO prices_latest (height, timestamp, rowan_cusdt, token_prices, token_volumes_24hr)
            VALUES ({0}, '{1}', {2}, '{3}', '{4}');

            delete from prices_latest
            where height < '{0}';

            """.format(height, timestamp, rowan_cusdt,
                       json.dumps(token_prices_dict), json.dumps(token_volumes_dict))

    database_service.execute_update(sql_str)
