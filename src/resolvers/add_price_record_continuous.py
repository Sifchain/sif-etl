from resolvers.add_price_record_pmtp import add_price_record_pmtp_resolver


def add_price_record_continuous_resolver():
    while (True):
        add_price_record_pmtp_resolver()
