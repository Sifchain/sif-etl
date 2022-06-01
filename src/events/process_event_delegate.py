from mutations.create_event_delegate import create_event_delegate_mutation
from utils import clean_parse_amount_util


def process_event_delegate_event(hash, event_type, events, height, timestamp, tx):
    validator_addr = ''
    sender_addr = ''
    amount = None
    raw_amount = ""
    transferObj = {}
    delegateObj = {}
    for event in events:
        if event["type"] == "delegate":
            delegateObj = event["attributes"]
        if event["type"] == "transfer":
            transferObj = event["attributes"]

    for obj in delegateObj:
        if obj['key'] == 'validator':
            validator_addr = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value']
            amount = clean_parse_amount_util(raw_amount)/10**18

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    for obj in transferObj:
        if obj['key'] == 'sender':
            sender_addr = obj['value']

    create_event_delegate_mutation(hash, event_type, events,  height, timestamp,
                                   validator_addr, sender_addr, amount, gasWanted, gasUsed)
