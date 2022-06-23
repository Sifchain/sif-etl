from src.mutations.create_event_proposal_deposit import create_event_proposal_deposit_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util


def process_event_proposal_deposit_event(hash, event_type, events, height, timestamp, token_decimal_dict, tx):

    amount = None
    transferObj = {}
    senderObj = {}
    raw_amount = ""
    sender = ""
    recipient = ""

    proposalObj = {}
    for event in events:
        if event["type"] == "proposal_deposit":
            transferObj = event["attributes"]
        if event["type"] == "transfer":
            senderObj = event["attributes"]
        if event["type"] == "submit_proposal":
            proposalObj = event["attributes"]

    for obj in transferObj:
        if obj['key'] == 'amount':
            raw_amount = obj['value']

    proposal_type = ""
    voting_period_start = ""
    for obj in proposalObj:
        if obj['key'] == "proposal_type":
            proposal_type = obj['value']
        if obj['key'] == 'voting_period_start':
            voting_period_start = obj['value']

    for obj in senderObj:
        if obj['key'] == 'sender':
            sender = obj['value']
        if obj['key'] == 'recipient':
            recipient = obj['value']

    token = clean_parse_token_util(raw_amount)
    if token == '':
        token = 'rowan'
    token_decimals = token_decimal_dict[token]

    amount = clean_parse_amount_util(raw_amount)/10**token_decimals

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_proposal_deposit_mutation(hash, event_type, events,  height, timestamp,
                                           sender, recipient, proposal_type, voting_period_start, token, amount, gasWanted, gasUsed)
