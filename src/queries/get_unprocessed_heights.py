import logging

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("get_unprocessed_heights_query", formatter)


def get_unprocessed_tokenprices_heights_query(latest_height):
    sql_str = """
        SELECT
          generate_series FROM GENERATE_SERIES
          (
            (6539609), ({0})
          ) 
        WHERE
          NOT EXISTS(SELECT height FROM tokenprices WHERE height = generate_series and height > 6539609)
          order by generate_series
    """.format(latest_height)
    logger.info(sql_str)
    database_service.cursor.execute(sql_str)
    records = [r[0] for r in database_service.cursor.fetchall()]
    return records


def get_unprocessed_heights_query_testnet(latest_height, start_height=None, event_types: [] = None):
    if start_height is None:
        sql_str = """
            SELECT
              generate_series FROM GENERATE_SERIES
              (
                (select min(height) from events_audit where height > 10000 
                and "type" in('lppd/distribution','rewards/distribution')), ({0})
              ) 
            WHERE
              NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series 
              and "type" in('lppd/distribution','rewards/distribution'))
              order by generate_series
        """.format(latest_height)
    else:
        if event_types is None:
            sql_str = """
            SELECT
                  generate_series FROM GENERATE_SERIES
                  (
                    ({0}), ({1})
                  ) 
                WHERE
                  NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series 
                  and "type" in('lppd/distribution','rewards/distribution'))
                  order by generate_series
            """.format(start_height, latest_height)
        else:
            event_filter = " type in ('" + "','".join(event_types) + "')"
            sql_str = f"""
            SELECT
                  generate_series FROM GENERATE_SERIES
                  (
                    ({start_height}), ({latest_height})
                  ) 
                WHERE
                  NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series                  
                  and {event_filter})
                  order by generate_series
            """

    logger.info(sql_str)
    database_service.cursor.execute(sql_str)
    records = [r[0] for r in database_service.cursor.fetchall()]
    return records


def get_unprocessed_heights_query(latest_height, start_height=None, event_type=None):
    if start_height is None:
        sql_str = """
            SELECT
              generate_series FROM GENERATE_SERIES
              (
                (select min(height) from events_audit where height > 2556371), ({0})
              ) 
            WHERE
              NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series )
              order by generate_series
        """.format(latest_height)
    else:
        if event_type is None:
            sql_str = """
            SELECT
                  generate_series FROM GENERATE_SERIES
                  (
                    ({0}), ({1})
                  ) 
                WHERE
                  NOT EXISTS(SELECT height FROM events_audit WHERE height = generate_series)
                  order by generate_series
            """.format(start_height, latest_height)
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
