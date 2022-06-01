from mutations.create_event_distribution_started import create_event_distribution_started_mutation
from utils import clean_parse_amount_util, clean_parse_token_util


def process_event_distribution_started_event(hash, event_type, events, height, timestamp, token_decimal_dict, tx):

    amount = None
    raw_amount = ""

    messageObj = {}
    transferObj = {}
    for event in events:
        if event["type"] == "transfer":
            transferObj = event["attributes"]
        if event["type"] == "message":
            messageObj = event["attributes"]

    sender = ""
    recipient = ""
    for obj in transferObj:
        if obj['key'] == 'recipient':
            recipient = obj['value']
        if obj['key'] == 'sender':
            sender = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value']

    action = ""
    for obj in messageObj:
        if obj['key'] == 'action':
            action = obj['value']

    token = clean_parse_token_util(raw_amount)
    if token == '':
        token = 'rowan'
    token_decimals = token_decimal_dict[token]

    amount = clean_parse_amount_util(raw_amount)/10**token_decimals

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_distribution_started_mutation(hash, event_type, events,  height, timestamp,
                                               sender, recipient, action,
                                               token, amount, gasWanted, gasUsed)
