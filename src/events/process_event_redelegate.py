from utils import clean_parse_amount_util, clean_parse_token_util
from mutations.create_event_redelegate import create_event_redelegate_mutation


def process_event_redelegate_event(hash, event_type, events, height, timestamp, token_decimal_dict, tx):
    # TODO: Work on processing this event

    recipient_addr = ''
    sender_addr = ''
    amount = None
    transferObj = {}
    raw_amount = ""
    redelegateObj = {}
    messageObj = {}

    for event in events:
        if event["type"] == "transfer":
            transferObj = event["attributes"]
        if event["type"] == "redelegate":
            redelegateObj = event["attributes"]
        if event["type"] == "message":
            messageObj = event["attributes"]

    for obj in transferObj:
        if obj['key'] == 'recipient':
            recipient_addr = obj['value']
        if obj['key'] == 'sender':
            sender_addr = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value']

    for obj in redelegateObj:
        if obj["key"] == "source_validator":
            source_validator = obj['value']
        if obj["key"] == "destinition_validator":
            destination_validator = obj['value']

    if raw_amount != "":
        token = clean_parse_token_util(raw_amount)
        token_decimals = token_decimal_dict[token]
        amount = clean_parse_amount_util(raw_amount)/10**token_decimals

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_redelegate_mutation(hash, event_type, events,  height, timestamp, source_validator, destination_validator,
                                     recipient_addr, sender_addr, token, amount, gasWanted, gasUsed)
