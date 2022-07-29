from src.services.database import database_service


def get_latest_processed_tokenprices_height_query():
    sql_str = """
        select max(height) from tokenprices
    """
    return database_service.execute_scalar(sql_str)


def get_latest_processed_height_query(is_lpd: int = None):
    sql_str = """
        select max(height) from events_audit
    """
    if is_lpd:
        sql_str = """
                select max(height) from events_audit_rewards where "type" in('lppd/distribution','rewards/distribution')
            """
    return database_service.execute_scalar(sql_str)
