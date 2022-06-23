from src.services.database import database_service


def get_token_price_rowan_query(token_symbol):
    token_price_query = """
        WITH s AS
            (select (token_prices->>'{0}_rowan')::numeric as {0}_rowan from prices order by height DESC LIMIT 5)
            SELECT avg({0}_rowan) FROM s;
        """.format(
        token_symbol
    )
    token_price = database_service.execute_query(token_price_query)[0]["avg"]
    return token_price
