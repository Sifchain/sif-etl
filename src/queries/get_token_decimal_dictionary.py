from queries.get_token_decimal_dictionary_db import get_token_decimal_dictionary_db_query


def get_token_decimal_dictionary_query():
    token_registry = get_token_decimal_dictionary_db_query()
    token_decimal_dict = {}
    for token in token_registry:
        token_decimal_dict[token["hash_symbol"].lower()] = token["decimals"]

    return token_decimal_dict
