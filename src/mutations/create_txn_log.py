from services.config import config_service
from services import database_service


def create_txn_log_mutation(hash, id, height, timestamp, txn_type,
                            validator, recipient, sender, amount, token, txn_sequence_no
                            ):

    if amount is None:
        sql_str = """
        INSERT INTO {9}
        (events_audit_id, height, time, txn_type, validator, hash, recipient, sender, txn_sequence_no)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
        """.format(id, height, timestamp, txn_type, validator, hash, recipient, sender, txn_sequence_no, config_service.schema_config['EVENT_TXN_TABLE'])
    else:
        sql_str = """
        INSERT INTO {11}
        (events_audit_id, height, time, 
        txn_type, amount, token, 
        validator, hash, recipient, sender, txn_sequence_no)
        VALUES ('{0}', '{1}', '{2}', 
        '{3}', '{4}', '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        """.format(id, height, timestamp,
                   txn_type, amount, token,
                   validator, hash, recipient, sender, txn_sequence_no,
                   config_service.schema_config['EVENT_TXN_TABLE'])

    database_service.execute_update(sql_str)
