import ciso8601

from src.mutations.create_event_user_claims import create_event_user_claims_mutation


def process_event_user_claim_event(hash, event_type, events, height, timestamp):

    claimObj = {}
    for event in events:
        if event['type'] == 'userClaim_new':
            claimObj = event['attributes']

    address = None
    claim_type = None
    claim_time_raw = ""

    for claim in claimObj:
        if claim['key'] == "userClaim_creator":
            address = claim['value']
        if claim['key'] == "userClaim_type":
            claim_type = claim['value']
        if claim['key'] == "userClaim_creationTime":
            claim_time_raw = claim['value']

    tm = ciso8601.parse_datetime(claim_time_raw)
    claim_time = tm.timestamp()

    create_event_user_claims_mutation(height, hash, event_type, timestamp,
                                      address, claim_type, claim_time, events, claim_time_raw)
