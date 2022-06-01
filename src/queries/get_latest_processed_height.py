from services import config_service
from services import database_service


def get_latest_processed_height_query():
    sql_str = """
        select max(height) from {0}
    """.format(config_service.schema_config['EVENTS_TABLE_V2'])

    return database_service.execute_scalar(sql_str)
