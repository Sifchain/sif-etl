from src.services.database import database_service


def get_claims_heights_query():
    sql_str = """
    select height from events_audit where type = 'userClaim_new'
    and description = 'UNKNOWN'
    """
    database_service.cursor.execute(sql_str)
    records = [r[0] for r in database_service.cursor.fetchall()]
    return records
