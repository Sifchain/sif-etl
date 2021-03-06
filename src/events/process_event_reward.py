import re

from src.mutations.create_events import *
from src.utils.clean_parse_amount import clean_parse_amount_util


def process_event_record_rewards_event(_hash, event_type, events, height, timestamp, token_decimal_dict) -> None:
    recipient_addr = ''
    sender_addr = ''
    amount = None
    raw_amount = None
    token = None
    transferObj = {}
    msgObj = {}
    withdrawObj = {}

    for event in events:
        if event["type"] == "message":
            msgObj = event["attributes"]
        if event["type"] == "transfer":
            transferObj = event["attributes"]
        if event["type"] == "withdraw_rewards":
            withdrawObj = event["attributes"]

    for obj in transferObj:
        try:
            if obj['key'] == 'recipient':
                recipient_addr = obj['value']
            if obj['key'] == 'sender':
                sender_addr = obj['value']
            if obj['key'] == 'amount':
                raw_amount = obj['value']
        except KeyError:
            continue

    for obj in withdrawObj:
        try:
            if event_type == "withdraw_rewards":
                if obj["key"] == "validator":
                    recipient_addr = obj["value"]
            if obj["key"] == "amount":
                raw_amount = obj["value"]
        except KeyError:
            continue

    for obj in msgObj:
        if obj["key"] == "sender":
            sender_addr = obj["value"]

    if raw_amount is None:
        token = None
        amount = None
    else:
        token = re.sub('[0-9]', '', str(raw_amount)).strip()
        token_decimals = token_decimal_dict[token]
        amount = clean_parse_amount_util(raw_amount) / 10 ** token_decimals

    create_event_rewards_mutation(_hash, event_type, events, height, timestamp, recipient_addr, sender_addr, amount,
                                  token)
