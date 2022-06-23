import json
import logging

from src.queries.get_token_decimal_dictionary_db import get_token_decimal_dictionary_db_query
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("process_event_txn_resolver", formatter)


def process_event_txn_resolver(txn_events):
    token_decimal_dict = get_token_decimal_dictionary_db_query()
    for txn_event in txn_events:
        height = txn_event['height']
        event_id = txn_event['id']
        txns = txn_event["log"]
        timestamp = txn_event['time']
        try:
            hash = ""
            txn_sequence_no = 0
            txnObj = {}
            for txn in txns:
                try:
                    txnObj = {}
                    txn_type = txn["type"]
                    txnAttr = []

                    for attr in txn["attributes"]:
                        key = decode_hash_util(attr['key'])
                        value = decode_hash_util(attr['value'])
                        txnAttr.append({"key": key, "value": value})

                    txnObj = {
                        "type": txn_type,
                        "attr": txnAttr
                    }

                    payload = {
                        "event_audit_id": event_id,
                        "height": height,
                        "txn_type": txn_type,
                        "txn_obj": txnObj,
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    }

                    hash = create_hash_util(json.dumps(payload), "")

                    amount = None
                    validator = ""
                    recipient = ""
                    sender = ""
                    token = ""
                    raw_amount = None

                    for attr in txnObj['attr']:
                        if txn_type == 'transfer':
                            if attr['key'] == 'recipient':
                                recipient = attr['value']
                            if attr['key'] == 'sender':
                                sender = attr['value']
                        if attr['key'] == 'amount':
                            raw_amount = attr['value']

                        if attr['key'] == 'validator':
                            validator = attr['value']

                    if raw_amount is not None:
                        token = clean_parse_token_util(raw_amount)
                        if token == '':
                            token = 'rowan'

                        token_decimals = -1
                        for token_reg in token_decimal_dict:
                            if token == token_reg['hash_symbol'].lower():
                                token_decimals = token_reg['decimals']

                        if token_decimals < 0:
                            raise ValueError("Couldn't find the token")

                        amount = clean_parse_amount_util(
                            raw_amount)/10**token_decimals

                    create_txn_log_mutation(hash, event_id, height, timestamp, txn_type,
                                            validator, recipient, sender, amount, token, txn_sequence_no)
                    txn_sequence_no += 1

                except Exception as e:
                    logger.critical(
                        f"Partial Transaction successful.  Mark this height as partial {height} txn = {txnObj}")
                    raise ValueError()

        except ValueError as e:
            logger.critical(
                f"Rollback partial successful txn error {e} at height: {height}")
            rollback_partial_txn_mutation(event_id)

        except Exception as e:
            logger.critical(
                f"Other exception detected: {e}  Skipping at {height}")
