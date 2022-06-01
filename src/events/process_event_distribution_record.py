from mutations.create_event_post_distribution import create_event_post_distribution_mutation
from events.process_event_distribution_started import process_event_distribution_started_event
from utils import clean_parse_amount_util


def process_event_distribution_record_event(hash, event_type, events, height, timestamp, token_decimal_dict, tx):

    dispObj = {}
    dispRunObj = {}

    distribution_rec = []
    raw_amount = None
    recipient = None
    disp_type = None

    for event in events:
        if event["type"] == "distribution_run":
            dispRunObj = event["attributes"]
        if event["type"].startswith('distribution_record'):
            for obj in event["attributes"]:
                if obj["key"] == "recipient_address":
                    recipient = obj["value"]
                if obj["key"] == "type":
                    disp_type = obj["value"]
                if obj["key"] == "amount":
                    raw_amount = obj["value"]

            if recipient is not None and disp_type is not None and raw_amount is not None:
                amount = clean_parse_amount_util(raw_amount)/10**18
                dispObj = {
                    "recipient": recipient,
                    "disp_type": disp_type,
                    "amount": amount
                }
                distribution_rec.append(dispObj)

    distribution_name = None
    for disp in dispRunObj:
        if disp["key"] == "distribution_name":
            distribution_name = disp["value"]

    create_event_post_distribution_mutation(
        height, timestamp, distribution_rec, distribution_name)
    process_event_distribution_started_event(
        hash, event_type, events, height, timestamp, token_decimal_dict, tx)
