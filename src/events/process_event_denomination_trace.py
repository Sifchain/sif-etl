from src.mutations.create_events import create_event_denomination_trace_mutation


def process_event_denomination_trace_event(hash, event_type, events, height, timestamp):

    amount = None
    sender = ""
    receiver = ""
    denom = ""
    success = None

    denom_traceObj = {}
    fungible_tokenObj = {}
    recv_packetObj = {}
    transfer_obj = {}

    for event in events:
        if event["type"] == "denomination_trace":
            denom_traceObj = event["attributes"]
        if event["type"] == "fungible_token_packet":
            fungible_tokenObj = event["attributes"]
        if event["type"] == "recv_packet":
            recv_packetObj = event["attributes"]
        if event["type"] == "transfer":
            transfer_obj = event["attributes"]

    for obj in denom_traceObj:
        if obj["key"] == "denom":
            denom = obj["value"].lower()

    for obj in fungible_tokenObj:
        if obj["key"] == "receiver":
            receiver = obj["value"]
        if obj["key"] == "amount":
            amount = float(obj["value"])
        if obj["key"] == "success":
            success = bool(obj["value"])

    packet_timeout_height = ""
    packet_timeout_timestamp = ""
    packet_sequence = ""
    packet_src_port = ""
    packet_src_channel = ""
    packet_dst_port = ""
    packet_dst_channel = ""
    packet_channel_ordering = ""
    packet_connection = ""

    for obj in recv_packetObj:
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

    create_event_denomination_trace_mutation(hash, event_type, events,  height, timestamp,
                                             sender, receiver, denom, amount, success, packet_src_port,
                                             packet_src_channel, packet_dst_port, packet_dst_channel, packet_channel_ordering,
                                             packet_connection, packet_timeout_timestamp, packet_timeout_height, packet_sequence)
