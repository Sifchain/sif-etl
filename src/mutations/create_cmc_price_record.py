import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("create_cmc_price_record_batch_mutation", formatter)


def create_cmc_price_record_mutation(timestamp, token, circulating_supply, total_supply,
                                     last_updated, cmc_rank, last_price, volume_24h, percent_change_1h, percent_change_24h,
                                     percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d,
                                     market_cap, is_active):

    sql_str = """
    UPDATE tokenprices_coinmarketcap
    set is_latest = false
    where token = '{1}'
    and timestamp < '{0}'
    and is_latest = true
    """.format(timestamp, token)

    database_service.execute_update(sql_str)

    if is_active:
        sql_str = '''
        INSERT INTO tokenprices_coinmarketcap
        (timestamp, token, circulating_supply, total_supply,
            last_updated, cmc_rank, last_price, volume_24h, percent_change_1h, percent_change_24h,
            percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d,
            market_cap)
        VALUES ('{0}', '{1}', '{2}', '{3}', 
        '{4}', '{5}', '{6}', '{7}', '{8}', 
        '{9}', '{10}', '{11}', '{12}',
        '{13}', 
        '{14}')
        '''.format(timestamp, token, circulating_supply, total_supply,
                   last_updated, cmc_rank, last_price, volume_24h, percent_change_1h,
                   percent_change_24h, percent_change_7d, percent_change_30d, percent_change_60d,
                   percent_change_90d,
                   market_cap)
    else:
        sql_str = '''
        INSERT INTO tokenprices_coinmarketcap
        (timestamp, token, 
            last_updated
            )
        VALUES ('{0}', '{1}',  
        '{2}')
        '''.format(timestamp, token, last_updated)

    database_service.execute_update(sql_str)
