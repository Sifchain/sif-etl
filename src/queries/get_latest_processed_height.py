from src.services.database import database_service


def get_latest_processed_height_query():
    sql_str = """
        select max(height) from events_audit
    """

    return database_service.execute_scalar(sql_str)
