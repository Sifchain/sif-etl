from mutations.create_event_create_claim import create_event_create_claim_mutation
from utils import clean_parse_token_util, clean_parse_amount_util


def process_event_create_claim_event(hash, event_type, events, height, timestamp, token_decimal_dict):

    claim_type = ""
    module = ""
    prophecy_status = ""
    transferObj = {}

    for event in events:
        if event['type'] == 'message':
            for attr in event['attributes']:
                if attr["key"] == "action":
                    claim_type = attr["value"]
                elif attr["key"] == "module":
                    module = attr["value"]
        if event["type"] == 'prophecy_status':
            for attr in event['attributes']:
                if attr['key'] == 'status':
                    prophecy_status = attr['value']
        if event['type'] == 'transfer':
            transferObj = event['attributes']

    recipient_addr = ''
    sender_addr = ''
    raw_amount = None
    for obj in transferObj:
        if obj['key'] == 'recipient':
            recipient_addr = obj['value']
        if obj['key'] == 'sender':
            sender_addr = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value']

    if raw_amount is None:
        amount = None
        token = ''
    else:
        token = clean_parse_token_util(raw_amount)
        token_decimals = token_decimal_dict[token]
        amount = clean_parse_amount_util(raw_amount)/10**token_decimals

    create_event_create_claim_mutation(hash, event_type, events, height, timestamp,
                                       recipient_addr, sender_addr, amount, token,
                                       claim_type, module, prophecy_status
                                       )
