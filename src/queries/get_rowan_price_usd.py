from src.services.database import database_service


def get_rowan_price_usd_query():
    get_rowan_price_query = """
        WITH s AS
            (SELECT rowan_cusdt FROM prices ORDER BY height DESC LIMIT 5)
            SELECT avg(rowan_cusdt) FROM s;
        """
    rowan_price = database_service.execute_query(
        get_rowan_price_query)[0]["avg"]
    return rowan_price
