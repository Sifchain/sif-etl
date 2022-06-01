import logging
from services import config_service
from services import database_service
from utils import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("get_unprocessed_heights_query", formatter)


def get_unprocessed_heights_query(latest_height, start_height=None, event_type=None):

    if start_height is None:
        sql_str = """
            SELECT
              generate_series FROM GENERATE_SERIES
              (
                (select min(height) from {0} where height > 2556371), ({1})
              ) 
            WHERE
              NOT EXISTS(SELECT height FROM {0} WHERE height = generate_series 
              and type in ('request_unlock_liquidity', 'cancel_unlock_liquidity') )
              order by generate_series
        """.format(config_service.schema_config['EVENTS_TABLE_V2'], latest_height)
    else:
        if event_type is None:
            sql_str = """
            SELECT
                  generate_series FROM GENERATE_SERIES
                  (
                    ({0}), ({1})
                  ) 
                WHERE
                  NOT EXISTS(SELECT height FROM {2} WHERE height = generate_series)
                  order by generate_series
            """.format(start_height, latest_height, config_service.schema_config['EVENTS_TABLE_V2'])
        else:
            sql_str = f"""
            SELECT
                  generate_series FROM GENERATE_SERIES
                  (
                    ({start_height}), ({latest_height})
                  ) 
                WHERE
                  NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series and type like '%{event_type}%')
                  order by generate_series
            """

    logger.info(sql_str)
    database_service.cursor.execute(sql_str)
    records = [r[0] for r in database_service.cursor.fetchall()]
    return records
