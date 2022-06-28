from src.mutations.create_events import create_event_transaction_mutation
from src.utils.clean_parse_amount import clean_parse_amount_util
from src.utils.clean_parse_token import clean_parse_token_util


def process_event_ibc_transfer_event(hash, event_type, events, height, timestamp):
    amount = None
    sender = ""
    receiver = ""
    denom = ""
    success = True

    send_packetObj = {}
    transfer_obj = {}

    for event in events:
        if event["type"] == "send_packet":
            send_packetObj = event["attributes"]
        if event["type"] == "transfer":
            transfer_obj = event["attributes"]

    packet_timeout_height = ""
    packet_timeout_timestamp = ""
    packet_sequence = ""
    packet_src_port = ""
    packet_src_channel = ""
    packet_dst_port = ""
    packet_dst_channel = ""
    packet_channel_ordering = ""
    packet_connection = ""

    raw_amount = ""
    for obj in send_packetObj:
        if obj["key"] == "packet_timeout_height":
            packet_timeout_height = obj["value"]
        if obj["key"] == "packet_timeout_timestamp":
            packet_timeout_timestamp = obj["value"]
        if obj["key"] == "packet_sequence":
            packet_sequence = obj["value"]

        if obj["key"] == "packet_src_port":
            packet_src_port = obj["value"]
        if obj["key"] == "packet_src_channel":
            packet_src_channel = obj["value"]
        if obj["key"] == "packet_dst_port":
            packet_dst_port = obj["value"]
        if obj["key"] == "packet_dst_channel":
            packet_dst_channel = obj["value"]
        if obj["key"] == "packet_channel_ordering":
            packet_channel_ordering = obj["value"]
        if obj["key"] == "packet_connection":
            packet_connection = obj["value"]

    for obj in transfer_obj:
        if obj["key"] == "sender":
            sender = obj["value"]
        if obj["key"] == "recipient":
            receiver = obj["value"]
        if obj["key"] == "amount":
            raw_amount = obj["value"]
            denom = clean_parse_token_util(raw_amount)
            amount = clean_parse_amount_util(raw_amount)

    create_event_transaction_mutation(hash, event_type, events, height, timestamp,
                                      sender, receiver, denom, amount, success, packet_src_port,
                                      packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
                                      packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence)
