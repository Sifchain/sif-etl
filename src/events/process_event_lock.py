from utils import clean_parse_amount_util, clean_parse_token_util
from mutations.create_event_add_lock import create_event_add_lock_mutation


def process_event_lock_event(hash, event_type, events, height, timestamp, token_decimal_dict):

    transferObj = {}
    for event in events:
        if event["type"] == "transfer":
            transferObj = event["attributes"]

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
        lk_token = clean_parse_token_util(raw_amount[0])
        lk_token_decimals = token_decimal_dict[lk_token]

        lk_amount = clean_parse_amount_util(
            raw_amount[0])/10**lk_token_decimals
        lk_token2 = clean_parse_token_util(raw_amount[1])
        lk_token_decimals2 = token_decimal_dict[lk_token2]
        lk_amount2 = clean_parse_amount_util(
            raw_amount[1])/10**lk_token_decimals2
    else:
        lk_token = clean_parse_token_util(raw_amount[0])
        lk_token_decimals = token_decimal_dict[lk_token]
        lk_amount = clean_parse_amount_util(
            raw_amount[0])/10**lk_token_decimals
        lk_token2 = ''
        lk_amount2 = None

    create_event_add_lock_mutation(hash, event_type, events, height, timestamp,
                                   recipient_addr, sender_addr, lk_amount, lk_token, lk_amount2,  lk_token2)
