from src.resolvers.add_liquidity_provider import add_liquidity_provider_pmtp_resolver


def add_pool_record_continuous_resolver():
    while True:
        add_liquidity_provider_pmtp_resolver()
