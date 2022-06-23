import re

from src.mutations.create_event_edit_validator import create_event_edit_validator_mutation


def process_event_edit_validator_event(hash, event_type, events, height, timestamp, tx):

    transferObj = {}
    senderObj = {}

    for event in events:
        if event["type"] == "edit_validator":
            transferObj = event["attributes"]
        if event["type"] == "message":
            senderObj = event["attributes"]

    raw_commission_rate = ""
    raw_min_self_delegation = ""
    for obj in transferObj:
        if obj['key'] == 'commission_rate':
            raw_commission_rate = obj['value']
        if obj['key'] == 'min_self_delegation':
            raw_min_self_delegation = obj['value']

    sender = ""
    for obj in senderObj:
        if obj['key'] == 'sender':
            sender = obj['value']

    commission_rate = float(re.findall(
        r"\srate: \"(\d*\.?\d+)\"", str(raw_commission_rate))[0])

    max_commission_rate = float(re.findall(
        r"max_rate: \"(\d*\.?\d+)\"", str(raw_commission_rate))[0])

    max_commission_change_rate = float(re.findall(
        r"max_change_rate: \"(\d*\.?\d+)\"", str(raw_commission_rate))[0])
    min_self_delegation = int(raw_min_self_delegation)

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_edit_validator_mutation(hash, event_type, events,  height, timestamp,
                                         sender, min_self_delegation, commission_rate, max_commission_change_rate, max_commission_rate,
                                         gasWanted, gasUsed)
