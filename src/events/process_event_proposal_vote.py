from src.mutations.create_event_proposal_vote import create_event_proposal_vote_mutation


def process_event_proposal_vote_event(hash, event_type, events, height, timestamp, tx):

    sender = ""

    transferObj = {}
    senderObj = {}
    for event in events:
        if event["type"] == "proposal_vote":
            transferObj = event["attributes"]

        if event["type"] == "message":
            senderObj = event["attributes"]

    vote = ""
    for obj in transferObj:
        if obj['key'] == 'option':
            vote = obj['value']

    for obj in senderObj:
        if obj['key'] == 'sender':
            sender = obj['value']

    gasWanted = float(tx["gas_wanted"])/10**18
    gasUsed = float(tx['gas_used'])/10**18

    create_event_proposal_vote_mutation(hash, event_type, events,  height, timestamp,
                                        sender, vote, gasWanted, gasUsed)
