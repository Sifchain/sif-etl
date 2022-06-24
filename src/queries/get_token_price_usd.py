from src.services.database import database_service


def get_token_price_usd_query(token_symbol):
    token_price_query = """
    with s as           
        (select asset_price::numeric as {0}_cusdt from TokenPrices
    where asset = 'rowan_cusdt' order by height desc limit 5 )
        select avg({0}_cusdt) from s;
        """.format(
        token_symbol
    )
    token_price = database_service.execute_query(token_price_query)[0]["avg"]
    return token_price
