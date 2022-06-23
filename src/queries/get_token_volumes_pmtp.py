from src.services.database import database_service


def get_token_volumes_pmtp_query():
    swap_query = """
        select ea.height, 
        tb.base_denom as swap_token_in,
        tf.base_denom as swap_token_out,
        ea.swap_begin_amount as swap_token_in_amount,
        ea.swap_final_amount as swap_token_out_amount,
        ea.swap_liquidity_fee
        from events_audit ea inner join token_registry tb on ea.swap_begin_token = lower(tb.denom)
        inner join token_registry tf on ea.swap_final_token = lower(tf.denom)
        where ea.time BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW()
        and ea.type = 'swap_successful'
        """

    swap_query_result = database_service.execute_query(swap_query)

    token_swap_dict = {}
    for swap in swap_query_result:
        token_swap_dict[swap["swap_token_in"]] = 0
        token_swap_dict[swap["swap_token_out"]] = 0

    for swap in swap_query_result:
        token_swap_dict[swap["swap_token_in"]] += swap["swap_token_in_amount"]
        token_swap_dict[swap["swap_token_out"]
                        ] += swap["swap_token_out_amount"]

    token_volumes_dict = {}

    token_conversion_rate_query = """
         select left(asset, length(asset)-6) as token, avg(asset_price) as price_rate
         from tokenprices
         where height in (select distinct height from tokenprices order by height desc limit 5)
         and asset like '%_cusdt'
         group by token
         order by token
    """
    token_conversion_rate = database_service.execute_query(
        token_conversion_rate_query)

    for token, units in token_swap_dict.items():
        rate = 1.0
        for token_rate in token_conversion_rate:
            if token == token_rate["token"]:
                rate = token_rate["price_rate"]

        # Token Volume is normalized to Rowan
        token_volumes_dict[token] = float(units) * float(rate)

    return token_volumes_dict
