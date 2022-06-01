from services import config_service
from services import database_service


def get_token_price_usd_query(token_symbol):
    token_price_query = """
    with s as           
        (select asset_price::numeric as {0}_cusdt from {1}
    where asset = 'rowan_cusdt' order by height desc limit 5 )
        select avg({0}_cusdt) from s;
        """.format(
        token_symbol, config_service.schema_config["TOKEN_PRICES_TABLE"]
    )
    token_price = database_service.execute_query(token_price_query)[0]["avg"]
    return token_price
