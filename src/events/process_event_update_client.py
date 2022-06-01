from mutations.create_event_update_client import create_event_update_client_mutation


def process_event_update_client_event(hash, event_type, events, height, timestamp):
    client_id = ""
    client_type = ""
    consensus_height = ""
    header = ""
    module = "ibc_client"

    for event in events:
        if event["type"] == "update_client":
            atts = event["attributes"]
            for att in atts:
                if att["key"] == "client_id":
                    client_id = att["value"]
                if att["key"] == "client_type":
                    client_type = att["value"]
                if att["key"] == "consensus_height":
                    consensus_height = att["value"]
                if att["key"] == "header":
                    header = att["value"]

    create_event_update_client_mutation(hash, event_type, events, height, timestamp,
                                        client_id, client_type, consensus_height, header, module)
