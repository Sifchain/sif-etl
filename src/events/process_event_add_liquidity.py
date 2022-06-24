import re

from src.mutations.create_events import *
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util


def process_event_add_liquidity_event(hash, event_type, events, height, timestamp, token_decimal_dict):
    al_provider = None
    raw_amount = []

    transferObj = {}
    headerObj = {}
    for event in events:
        if event["type"] == "transfer":
            transferObj = event['attributes']
        if event['type'] == "added_liquidity":
            headerObj = event['attributes']

    pool = ""
    for obj in headerObj:
        if obj['key'] == 'liquidity_provider':
            pool = obj['value']

    pool = re.findall(
        r'asset:<symbol:\"(.+)\" > liquidity_provider_units', str(pool))[0]
#    pool = re.findall(r"ExternalAsset: Symbol: (\w+)\n\t", str(pool))[0]

    for obj in transferObj:
        if obj['key'] == 'sender':
            al_provider = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value'].split(',')

    if len(raw_amount) == 0:
        for event in events:
            if event["type"] == "transfer":
                transferObj = event["attributes"]

        for obj in transferObj:
            if obj['key'] == 'sender':
                al_provider = obj['value']
            if obj['key'] == 'amount':
                raw_amount = obj['value'].split(',')

    if len(raw_amount) == 0 or al_provider == None:
        raise Exception

    if len(raw_amount) == 2:
        al_token = clean_parse_token_util(raw_amount[0])
        al_token_decimals = token_decimal_dict[al_token]

        al_amount = clean_parse_amount_util(
            raw_amount[0])/10**al_token_decimals
        al_token2 = clean_parse_token_util(raw_amount[1])
        al_token_decimals2 = token_decimal_dict[al_token2]
        al_amount2 = clean_parse_amount_util(
            raw_amount[1])/10**al_token_decimals2
    else:
        al_token = clean_parse_token_util(raw_amount[0])
        al_token_decimals = token_decimal_dict[al_token]
        al_amount = clean_parse_amount_util(
            raw_amount[0])/10**al_token_decimals
        al_token2 = ''
        al_amount2 = None

    create_event_add_liquidity_mutation(hash, event_type, events, height, timestamp,
                                        al_token, al_provider, al_amount, al_token2,  al_amount2, pool)
