import re


def clean_parse_amount_util(raw_amount):
    if 'ibc' in raw_amount:
        first_index = raw_amount.find('ibc', 0)
        return float(raw_amount[0:first_index])

    if 'cb20' in raw_amount:
        first_index = raw_amount.find('cb20', 0)
        return float(raw_amount[0:first_index])

    amount = float(re.findall(r"(\d*\.?\d+)", str(raw_amount))[0])
    return amount
