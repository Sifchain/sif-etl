from services import config_service
from services import database_service


def get_re_processed_heights_query():

    sql_str = """
         select height, type from process_temp t where 
         height not in (select distinct height from {0} ea where type in ('added_liquidity', 'removed_liquidity'))
         order by height
     """.format(config_service.schema_config['EVENTS_TABLE_V2'])
    database_service.cursor.execute(sql_str)
    records = [r[0] for r in database_service.cursor.fetchall()]
    return records
