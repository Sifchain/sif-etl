from src.mutations.create_events import create_event_add_burn_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util


def process_event_record_burn_event(hash, event_type, events, height, timestamp, token_decimal_dict):
    # 1134434
    transferObj = {}
    for event in events:
        if event['type'] == 'transfer':
            transferObj = event['attributes']
    recipient_addr = ''
    sender_addr = ''
    raw_amount = []
    for obj in transferObj:
        if obj['key'] == 'recipient':
            recipient_addr = obj['value']
        if obj['key'] == 'sender':
            sender_addr = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value'].split(',')

    if len(raw_amount) == 0:
        raise Exception

    if len(raw_amount) == 2:
        bn_token = clean_parse_token_util(raw_amount[0])
        bn_token_decimals = token_decimal_dict[bn_token]

        bn_amount = clean_parse_amount_util(
            raw_amount[0])/10**bn_token_decimals
        bn_token2 = clean_parse_token_util(raw_amount[1])
        bn_token_decimals2 = token_decimal_dict[bn_token2]
        bn_amount2 = clean_parse_amount_util(
            raw_amount[1])/10**bn_token_decimals2
    else:
        bn_token = clean_parse_token_util(raw_amount[0])
        bn_token_decimals = token_decimal_dict[bn_token]
        bn_amount = clean_parse_amount_util(
            raw_amount[0])/10**bn_token_decimals
        bn_token2 = ''
        bn_amount2 = None

    create_event_add_burn_mutation(hash, event_type, events, height, timestamp,
                                   recipient_addr, sender_addr, bn_amount, bn_token, bn_amount2,  bn_token2)
