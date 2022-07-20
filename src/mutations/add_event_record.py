from src.events.process_event_acknowledge_packet import process_event_acknowledge_packet_event
from src.events.process_event_liquidity_related import *
from src.events.process_event_cancel_unlock_liquidity import process_event_cancel_unlock_liquidity_event
from src.events.process_event_create_claim import process_event_create_claim_event
from src.events.process_event_create_validator import process_event_create_validator_event
from src.events.process_event_delegate import process_event_delegate_event
from src.events.process_event_denomination_trace import process_event_transaction_event
from src.events.process_event_distribution_record import process_event_distribution_record_event
from src.events.process_event_distribution_started import process_event_distribution_started_event
from src.events.process_event_edit_validator import process_event_edit_validator_event
from src.events.process_event_ibc_transfer import process_event_ibc_transfer_event
from src.events.process_event_lock import process_event_lock_event
from src.events.process_event_lppd import process_event_lppd_distribution
from src.events.process_event_proposal_deposit import process_event_proposal_deposit_event
from src.events.process_event_proposal_vote import process_event_proposal_vote_event
from src.events.process_event_record_burn import process_event_record_burn_event
from src.events.process_event_redelegate import process_event_redelegate_event
from src.events.process_event_request_unlock_liquidity import process_event_request_unlock_liquidity_event
from src.events.process_event_reward import process_event_record_rewards_event
from src.events.process_event_swap import process_event_swap_event
from src.events.process_event_unbond import process_event_unbond_event
from src.events.process_event_unknown import process_event_unknown_event
from src.events.process_event_update_client import process_event_update_client_event
from src.events.process_event_user_claim import process_event_user_claim_event
from src.mutations.create_events import create_event_unknown_tx_mutation
from src.queries.get_token_decimal_dictionary import get_token_decimal_dictionary_query
from src.services.sifapi import *
from src.utils.create_hash import create_hash_util
from src.utils.setup_logger import setup_logger_util

RPC_SERVER_URL = config_service.api_config["RPC_SERVER_URL"]
RPC_SERVER_TESTNET_URL = config_service.api_config["RPC_SERVER_TESTNET_URL"]

formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
logger = setup_logger_util("add_event_record_mutation", formatter)


def add_lddp_event_record_mutation(height: int = 1) -> None:
    try:
        block_result_url = "{0}/block_results?height={1}".format(RPC_SERVER_TESTNET_URL, height)
        data = requests.get(block_result_url).json()
        timestamp = get_timestamp_from_height_sifapi(height, 1)

        if data["result"].get("end_block_events", None):
            for event in data["result"]["end_block_events"]:
                try:
                    if event["type"] in ("lppd/distribution", "rewards/distribution"):
                        event_type = event["type"]
                        attrs = event["attributes"]
                        _hash = create_hash_util(json.dumps(attrs), timestamp)
                        process_event_lppd_distribution(_hash, event_type, attrs, height, timestamp)
                except Exception as e:
                    logger.critical(f"Data inserting error at {height} - {e}")

        return
    except Exception as e:
        logger.critical(f"Something bad at {height} - {e}")


def add_event_record_mutation(height=1):
    try:
        block_result_url = '{0}/block_results?height={1}'.format(RPC_SERVER_URL, height)
        data = requests.get(block_result_url).json()
        timestamp = get_timestamp_from_height_sifapi(height)

        if data['result'].get('txs_results', None) is None:
            try:
                if data.get('error', None) is not None:
                    return

                log_message = data.get('result', '')
                if log_message == '':
                    raise Exception("result is empty")

                _hash = create_hash_util(json.dumps(log_message), timestamp)

                events = log_message['begin_block_events']
                event_type = 'NO_TXN_TYPE'

                create_event_unknown_tx_mutation(
                    _hash, event_type, events, height, timestamp)
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
                except Exception:
                    logger.info(f"Unable to parse into json - {tx['log']}")
                    continue

                _hash = create_hash_util(json.dumps(tx['log']), timestamp)

                for message in log_message:
                    events = message["events"]
                    for event in events:
                        event_type = event['type']
                        if event_type in ['message', 'transfer', 'prophecy_status',
                                          'fungible_token_packet',
                                          'write_acknowledgement',
                                          'coin_received',
                                          'coin_spent',
                                          'recv_packet', 'send_packet']:
                            # These events are supplemental objects that will be processed later
                            """
                            Found a problem where the events array do not contain any of the header info

                            """
                            continue

                        # TODO: process event should be refactored as a class.

                        if event_type == 'delegate':
                            process_event_delegate_event(_hash, event_type, events, height, timestamp, tx)
                            continue

                        elif event_type == 'userClaim_new':
                            process_event_user_claim_event(_hash, event_type, events, height, timestamp)
                            continue

                        elif event_type == 'request_unlock_liquidity':
                            process_event_request_unlock_liquidity_event(_hash, event_type, events, height, timestamp,
                                                                         token_decimal_dict, tx)
                            continue

                        elif event_type in ('withdraw_rewards', 'withdraw_commission'):
                            process_event_record_rewards_event(_hash, event_type, events, height, timestamp,
                                                               token_decimal_dict)
                            continue

                        elif event_type == 'lock':
                            process_event_lock_event(_hash, event_type, events, height, timestamp, token_decimal_dict)
                            continue

                        elif event_type == 'update_client':
                            process_event_update_client_event(_hash, event_type, events, height, timestamp)
                            continue

                        elif event_type == 'acknowledge_packet':
                            process_event_acknowledge_packet_event(_hash, event_type, events, height, timestamp)
                            continue

                        elif event_type.startswith('distribution_record'):
                            process_event_distribution_record_event(_hash, event_type, events, height, timestamp,
                                                                    token_decimal_dict, tx)
                            continue

                        elif event_type == 'redelegate':
                            process_event_redelegate_event(_hash, event_type, events, height, timestamp,
                                                           token_decimal_dict, tx)
                            continue

                        elif event_type == 'burn':
                            process_event_record_burn_event(_hash, event_type, events, height, timestamp,
                                                            token_decimal_dict)
                            continue

                        elif event_type == 'unbond':
                            process_event_unbond_event(_hash, event_type, events, height, timestamp, token_decimal_dict)
                            continue

                        elif event_type == 'create_claim':
                            process_event_create_claim_event(_hash, event_type, events, height, timestamp,
                                                             token_decimal_dict)
                            continue

                        elif event_type == 'removed_liquidity':
                            process_event_remove_liquidity_event(_hash, event_type, events, height, timestamp,
                                                                 token_decimal_dict)
                            continue

                        elif event_type in ('added_liquidity', 'created_new_liquidity_provider'):
                            process_event_add_create_liquidity_event(_hash, event_type, events, height, timestamp,
                                                                     token_decimal_dict)
                            continue

                        elif event_type == 'swap_successful':
                            process_event_swap_event(_hash, event_type, events, height, timestamp, token_decimal_dict)
                            continue

                        elif event_type == 'create_validator':
                            process_event_create_validator_event(_hash, event_type, events, height, timestamp,
                                                                 token_decimal_dict, tx)
                            continue

                        elif event_type == 'edit_validator':
                            process_event_edit_validator_event(_hash, event_type, events, height, timestamp, tx)

                        elif event_type == 'proposal_vote':
                            process_event_proposal_vote_event(_hash, event_type, events, height, timestamp, tx)

                        elif event_type == 'distribution_started':
                            process_event_distribution_started_event(_hash, event_type, events, height, timestamp,
                                                                     token_decimal_dict, tx)

                        elif event_type == 'proposal_deposit':
                            process_event_proposal_deposit_event(_hash, event_type, events, height, timestamp,
                                                                 token_decimal_dict, tx)

                        elif event_type in ('denomination_trace', 'coinbase'):
                            process_event_transaction_event(_hash, event_type, events, height, timestamp)
                            continue

                        elif event_type == 'ibc_transfer':
                            process_event_ibc_transfer_event(_hash, event_type, events, height, timestamp)
                            continue

                        elif event_type == 'cancel_unlock_liquidity':
                            process_event_cancel_unlock_liquidity_event(_hash, event_type, events, height, timestamp,
                                                                        token_decimal_dict, tx)
                            continue

                        elif event_type == 'submit_proposal':
                            logger.critical(f"Already handled at proposal deposit at {height}")
                            continue

                        else:
                            logger.critical(f"Unknown Event:  {event_type} at {height}")
                            process_event_unknown_event(_hash, event_type, events, height, timestamp)
                            raise Exception(f"Unknown Event - {event_type}")

            except Exception as e:
                logger.critical(
                    f"Something bad at {height} - processing next message: {e}")

        return

    except Exception as e:
        logger.critical(f"Something bad at {height} - {e}")
