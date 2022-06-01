from services import config_service
from services import database_service


def get_rowan_price_usd_query():
    get_rowan_price_query = """
        WITH s AS
            (SELECT rowan_cusdt FROM {0} ORDER BY height DESC LIMIT 5)
            SELECT avg(rowan_cusdt) FROM s;
        """.format(
        config_service.schema_config["PRICES_TABLE"]
    )
    rowan_price = database_service.execute_query(
        get_rowan_price_query)[0]["avg"]
    return rowan_price
