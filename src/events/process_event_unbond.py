from utils import clean_parse_amount_util, clean_parse_token_util
from mutations.create_event_unbond import create_event_unbond_mutation


def process_event_unbond_event(hash, event_type, events, height, timestamp, token_decimal_dict):
    """
    [
  {
    "type": "message",
    "attributes": [
      { "key": "action", "value": "begin_unbonding" },
      { "key": "sender", "value": "sif1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8zzt2x5" },
      { "key": "sender", "value": "sif1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3sxxeku" },
      { "key": "module", "value": "staking" },
      { "key": "sender", "value": "sif13krafzesympu86kuls9m9z3945t3t5zwh0x5fg" }
    ]
  },
  {
    "type": "transfer",
    "attributes": [
      { "key": "recipient", "value": "sif13krafzesympu86kuls9m9z3945t3t5zwh0x5fg" },
      { "key": "sender", "value": "sif1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8zzt2x5" },
      { "key": "amount", "value": "7440236701973968rowan" },
      { "key": "recipient", "value": "sif1tygms3xhhs3yv487phx3dw4a95jn7t7lyx6gqg" },
      { "key": "sender", "value": "sif1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3sxxeku" },
      { "key": "amount", "value": "4208000000000000000000rowan" }
    ]
  },
  {
    "type": "unbond",
    "attributes": [
      { "key": "validator", "value": "sifvaloper1u5vffwarcqvmspcm6xkyt00f2j0nl6p756n4cg" },
      { "key": "amount", "value": "4208000000000000000000" },
      { "key": "completion_time", "value": "2021-05-17T18:25:36Z" }
    ]
  }
]
    """
    transferObj = {}
    messageObj = {}
    unbondObj = {}

    for event in events:
        if event["type"] == "transfer":
            transferObj = event['attributes']
        if event["type"] == "message":
            messageObj = event["attributes"]
        if event["type"] == "unbond":
            unbondObj = event["attributes"]

    transfer_events = []
    for obj in transferObj:
        transfer_events.append({obj['key']: obj['value']})

    begin_recipient_unbond = ""
    begin_sender_unbond = ""
    begin_amount_unbond = ""

    if len(transfer_events) > 0:
        begin_recipient_unbond = transfer_events[0]['recipient']
        begin_sender_unbond = transfer_events[1]['sender']
        begin_amount_unbond = transfer_events[2]['amount']
    else:
        for obj in unbondObj:
            if obj["key"] == "amount":
                begin_amount_unbond = obj["value"]
            if obj["key"] == "validator":
                begin_recipient_unbond = obj["value"]

        for obj in messageObj:
            if obj["key"] == "sender":
                begin_sender_unbond = obj["value"]

    final_recipient_unbond = ""
    final_sender_unbond = ""
    final_amount_unbond = ""
    final_amount_token = ""
    final_amount_token_in_dec = ""
    final_amount = None

    if len(transfer_events) > 4:
        final_recipient_unbond = transfer_events[3]['recipient']
        final_sender_unbond = transfer_events[4]['sender']
        final_amount_unbond = transfer_events[5]['amount']
        final_amount_token = clean_parse_token_util(final_amount_unbond)
        final_amount_token_in_dec = token_decimal_dict[final_amount_token]
        final_amount = clean_parse_amount_util(
            final_amount_unbond)/10**final_amount_token_in_dec

    if len(transfer_events) == 0:
        begin_amount_token = 'rowan'
        begin_amount = float(begin_amount_unbond) / \
            10**token_decimal_dict['rowan']
    else:
        begin_amount_token = clean_parse_token_util(begin_amount_unbond)
        begin_amount_token_in_dec = token_decimal_dict[begin_amount_token]
        begin_amount = clean_parse_amount_util(
            begin_amount_unbond)/10**begin_amount_token_in_dec

    create_event_unbond_mutation(hash, event_type, events, height, timestamp,
                                 begin_recipient_unbond, begin_sender_unbond, begin_amount, begin_amount_token,
                                 final_recipient_unbond, final_sender_unbond, final_amount, final_amount_token)
