import logging

from src.mutations.create_events import create_event_swap_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util(
    "process_event_swap_event", formatter)


def process_event_swap_event(hash, event_type, events, height, timestamp, token_decimal_dict):
    transfer_events = []
    transferObj = {}
    eventObjs = {}
    for obj in events:
        if obj["type"] == "transfer":
            transferObj = obj["attributes"]
        if obj["type"] == "swap_successful":
            eventObjs = obj["attributes"]

    begin_recipient_swap = ""
    begin_sender_swap = ""
    begin_amount_swap = ""

    final_recipient_swap = ""
    final_sender_swap = ""
    final_amount_swap = ""

    begin_amount_token = ""
    begin_amount_token_in_dec = 0
    begin_amount = 0

    final_amount_token = ""
    final_amount_token_in_dec = 0
    final_amount = 0

    try:
        for obj in transferObj:
            try:
                transfer_events.append({obj['key']: obj['value']})
            except Exception:
                continue

        begin_recipient_swap = transfer_events[0]['recipient']
        begin_sender_swap = transfer_events[1]['sender']
        begin_amount_swap = transfer_events[2]['amount']

        final_recipient_swap = transfer_events[3]['recipient']
        final_sender_swap = transfer_events[4]['sender']
        final_amount_swap = transfer_events[5]['amount']

        begin_amount_token = clean_parse_token_util(begin_amount_swap)
        begin_amount_token_in_dec = token_decimal_dict[begin_amount_token]
        begin_amount = clean_parse_amount_util(
            begin_amount_swap)/10**begin_amount_token_in_dec

        final_amount_token = clean_parse_token_util(final_amount_swap)
        final_amount_token_in_dec = token_decimal_dict[final_amount_token]
        final_amount = clean_parse_amount_util(
            final_amount_swap)/10**final_amount_token_in_dec

    except Exception:
        logger.info("Amount is missing probably.")
        logger.info(
            f"*************** {begin_amount_swap} - {final_amount_swap} {begin_sender_swap} - {begin_amount} {final_amount} - {final_sender_swap}")

    liquidity_fee = None
    price_impact = None
    for eventObj in eventObjs:
        if eventObj['key'] == 'liquidity_fee':
            liquidity_fee = float(eventObj['value'])
        if eventObj['key'] == 'price_impact':
            price_impact = float(eventObj['value'])

    liquidity_fee = liquidity_fee/10**final_amount_token_in_dec

    create_event_swap_mutation(hash, event_type, events, height, timestamp,
                               begin_recipient_swap, begin_sender_swap, begin_amount, begin_amount_token,
                               final_recipient_swap, final_sender_swap, final_amount, final_amount_token,
                               liquidity_fee, price_impact)
