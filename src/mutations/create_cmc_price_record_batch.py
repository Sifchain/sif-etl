import logging
from services.config import config_service
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_cmc_price_record_batch_mutation", formatter)


def create_cmc_price_record_batch_mutation(current_time, cmc):
    sql_str = """
        update tokenprices_coinmarketcap
        set is_latest = false
        where is_latest = true
        """

    database_service.execute_query(sql_str)

    for symbol in cmc["data"]:
        try:
            data = cmc["data"][symbol][0]
            is_active = data["is_active"] == 1
            circulating_supply = data["circulating_supply"]
            if circulating_supply is None:
                continue
            total_supply = data["total_supply"]
            last_updated = data["last_updated"]
            cmc_rank = data["cmc_rank"]
            usd_quote = data["quote"]["USD"]
            last_price = usd_quote["price"]

            volume_24h = usd_quote["volume_24h"]
            percent_change_1h = usd_quote["percent_change_1h"]
            percent_change_24h = usd_quote["percent_change_24h"]
            percent_change_7d = usd_quote["percent_change_7d"]
            percent_change_30d = usd_quote["percent_change_30d"]
            percent_change_60d = usd_quote["percent_change_60d"]
            percent_change_90d = usd_quote["percent_change_90d"]
            market_cap = usd_quote["market_cap"]
        except Exception as err:
            logger.fatal(
                f"Unable to parse with {err} - {symbol} - skipping")
            continue

        if is_active:
            sql_str = '''
                INSERT INTO {15}
                (timestamp, token, circulating_supply, total_supply,
                    last_updated, cmc_rank, last_price, volume_24h, percent_change_1h, percent_change_24h,
                    percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d,
                    market_cap)
                VALUES ('{0}', '{1}', '{2}', '{3}', 
                '{4}', '{5}', '{6}', '{7}', '{8}', 
                '{9}', '{10}', '{11}', '{12}',
                '{13}', 
                '{14}')
                '''.format(current_time, symbol, circulating_supply, total_supply,
                           last_updated, cmc_rank, last_price, volume_24h, percent_change_1h,
                           percent_change_24h, percent_change_7d, percent_change_30d, percent_change_60d,
                           percent_change_90d,
                           market_cap, config_service.schema_config['COINMARKETCAP_TABLE'])
            logger.info(sql_str)

        else:
            sql_str = '''
                INSERT INTO {3}
                (timestamp, token, 
                    last_updated
                    )
                VALUES ('{0}', '{1}',  
                '{2}')
                '''.format(current_time, symbol, last_updated, config_service.schema_config['COINMARKETCAP_TABLE'])
            logger.info(sql_str)

        database_service.execute_query(sql_str)

    sql_str = """
        delete from tokenprices_coinmarketcap
        where is_latest = false
        """

    database_service.execute_query(sql_str)
