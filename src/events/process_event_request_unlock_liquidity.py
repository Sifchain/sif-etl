from src.mutations.create_events import create_event_unlock_liquidity_mutation


def process_event_request_unlock_liquidity_event(_hash, event_type, events, height, timestamp, token_decimal_dict, tx):
    unlockObj = {}
    messageObj = {}
    for event in events:
        if event["type"] == "request_unlock_liquidity":
            unlockObj = event["attributes"]
        if event["type"] == "message":
            messageObj = event["attributes"]

    liquidity_provider = ""
    for obj in messageObj:
        if obj["key"] == "sender":
            liquidity_provider = obj["value"]

    pool = ""
    liquidity_units = ""
    for obj in unlockObj:
        if obj['key'] == 'pool':
            pool = obj['value']
        if obj['key'] == 'liquidity_units':
            liquidity_units = obj['value']

    create_event_unlock_liquidity_mutation(_hash, event_type, events, height, timestamp, liquidity_provider,
                                           liquidity_units, pool)
