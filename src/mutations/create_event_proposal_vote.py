import json
from services.config import config_service
from services import database_service


def create_event_proposal_vote_mutation(hash, event_type,
                                        events_arr, height, timestamp,
                                        sender, vote, gasWanted, gasUsed):

    sql_str = '''
    INSERT INTO {9}
    (hash, type, log, height, time,
    pv_sender, pv_vote, pv_gasWanted, pv_gasUsed)
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 
    '{5}', '{6}', '{7}', '{8}' 
    )
    '''.format(hash, event_type, json.dumps(events_arr), height, timestamp,
               sender, vote, gasWanted, gasUsed,
               config_service.schema_config['EVENTS_TABLE_V2'])

    database_service.execute_update(sql_str)
