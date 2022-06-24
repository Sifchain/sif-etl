import logging

from src.mutations.create_events import create_event_create_validator_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "process_event_create_validator_event", formatter)


def process_event_create_validator_event(hash, event_type, events, height, timestamp, token_decimal_dict, tx):

    logger.debug(f"Event:  {events}")

    amount = None
    transferObj = {}
    senderObj = {}
    raw_amount = ""
    validator = ""
    sender = ""

    for event in events:
        if event["type"] == "create_validator":
            transferObj = event["attributes"]
        if event["type"] == "message":
            senderObj = event["attributes"]

    for obj in transferObj:
        if obj['key'] == 'validator':
            validator = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value']

    for obj in senderObj:
        if obj['key'] == 'sender':
            sender = obj['value']

    token = clean_parse_token_util(raw_amount)
    if token == '':
        token = 'rowan'
    token_decimals = token_decimal_dict[token]

    amount = clean_parse_amount_util(raw_amount)/10**token_decimals

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_create_validator_mutation(hash, event_type, events,  height, timestamp,
                                           validator, sender, token, amount, gasWanted, gasUsed)
