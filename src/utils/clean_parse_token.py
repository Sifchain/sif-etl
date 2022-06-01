import re


def clean_parse_token_util(raw_amount):
    if 'ibc' in raw_amount:
        first_index = raw_amount.find('ibc', 0)
        return raw_amount[first_index:].lower()
    if 'cb20' in raw_amount:
        first_index = raw_amount.find('cb20', 0)
        return raw_amount[first_index:].lower()
    token = re.sub(r"(\d*\.?\d+)", '', raw_amount).strip()
    if token == 'cinch':
        token = 'c1inch'
    return token
