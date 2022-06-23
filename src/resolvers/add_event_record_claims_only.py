import json

from src.events.process_event_user_claim import process_event_user_claim_event
from src.queries.get_token_decimal_dictionary import get_token_decimal_dictionary_query
from src.services.sifapi import *
from src.utils.create_hash import create_hash_util
from src.utils.setup_logger import setup_logger_util

RPC_SERVER_URL = config_service.api_config["RPC_SERVER_URL"]

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_event_record_claims_only_resolver", formatter)


def add_event_record_claims_only_resolver(height=1):
    try:
        block_result_url = '{0}/block_results?height={1}'.format(
            RPC_SERVER_URL, height)

        data = requests.get(block_result_url).json()

        timestamp = get_timestamp_from_height_sifapi(height)

        if data['result'].get('txs_results', None) is None:
            try:
                if data.get('error', None) is not None:
                    return

                log_message = data.get('result', '')
                if log_message == '':
                    raise Exception("result is empty")

                hash = create_hash_util(json.dumps(log_message), timestamp)

                events = log_message['begin_block_events']
                event_type = 'NO_TXN_TYPE'


                return
            except Exception as e:
                logger.critical(f"Bad stuff - {height}: {e}")
                return

        token_decimal_dict = get_token_decimal_dictionary_query()

        error_msg = ['Unable to swap', 'user does not', 'out of gas', 'internal',
                     'insufficient', 'prophecy already', 'relegation to this validator',
                     'fail', 'panic']

        for tx in data['result']['txs_results']:
            try:
                ignore = False
                for e in error_msg:
                    if tx['log'].startswith(e):
                        ignore = True

                if ignore:
                    continue

                log_message = None
                try:
                    log_message = json.loads(tx["log"])
                except Exception as e:
                    logger.info(f"Unable to parse into json - {tx['log']}")
                    continue

                hash = create_hash_util(json.dumps(tx['log']), timestamp)

                for message in log_message:
                    events = message["events"]
                    logger.debug(events)
                    for event in events:
                        event_type = event['type']
                        if event_type in ['message', 'transfer', 'prophecy_status',
                                          'fungible_token_packet',
                                          'write_acknowledgement',
                                          'recv_packet', 'send_packet']:
                            # These events are supplemental objects that will be processed later
                            """
                            Found a problem where the events array do not contain any of the header info

                            """
                            continue

                        # TODO: process event should be refactored as a class.
                        if event_type == 'userClaim_new':
                            process_event_user_claim_event(
                                hash, event_type, events, height, timestamp)
                            continue
                        else:
                            continue

            except Exception as e:
                logger.critical(
                    f"Something bad at {height} - processing next message: {e}")

        return

    except Exception as e:
        logger.critical(f"Something bad at {height} - {e}")
