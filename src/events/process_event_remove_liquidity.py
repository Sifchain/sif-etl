import logging
import re

from src.mutations.create_events import create_event_remove_liquidity_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "process_event_remove_liquidity_event", formatter)


def process_event_remove_liquidity_event(hash, event_type, events, height, timestamp, token_decimal_dict):
    rl_provider = None
    raw_amount = []

    transferObj = {}
    headerObj = {}
    for event in events:
        if event["type"] == "transfer":
            transferObj = event['attributes']
        if event['type'] == "removed_liquidity":
            headerObj = event['attributes']

    pool = ""
    for obj in headerObj:
        if obj['key'] == 'liquidity_provider':
            pool = obj['value']

    pool = re.findall(
        r'asset:<symbol:\"(.+)\" > liquidity_provider_units', str(pool))[0]

    for obj in transferObj:
        if obj['key'] == 'recipient':
            rl_provider = obj['value']
        if obj['key'] == 'amount':
            raw_amount = obj['value'].split(',')

    if raw_amount is None or rl_provider is None:
        logger.debug(f"events: {events}")
        raise Exception

    if len(raw_amount) == 2:
        rl_token = clean_parse_token_util(raw_amount[0])
        rl_token_decimals = token_decimal_dict[rl_token]
        rl_amount = clean_parse_amount_util(
            raw_amount[0]) / 10 ** rl_token_decimals
        rl_token2 = clean_parse_token_util(raw_amount[1])
        rl_token_decimals2 = token_decimal_dict[rl_token2]
        rl_amount2 = clean_parse_amount_util(
            raw_amount[1]) / 10 ** rl_token_decimals2
    else:
        rl_token = clean_parse_token_util(raw_amount[0])
        rl_token_decimals = token_decimal_dict[rl_token]
        rl_amount = clean_parse_amount_util(
            raw_amount[0]) / 10 ** rl_token_decimals
        rl_token2 = ''
        rl_amount2 = None

    create_event_remove_liquidity_mutation(hash, event_type, events, height, timestamp,
                                           rl_token, rl_provider, rl_amount,
                                           rl_token2, rl_amount2, pool)
