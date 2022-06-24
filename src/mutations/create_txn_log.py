from src.services.database import database_service


def create_txn_log_mutation(hash, id, height, timestamp, txn_type,
                            validator, recipient, sender, amount, token, txn_sequence_no
                            ):

    if amount is None:
        sql_str = """
        insert into events_audit_txn
        (events_audit_id, height, time, txn_type, validator, hash, recipient, sender, txn_sequence_no)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
        """.format(id, height, timestamp, txn_type, validator, hash, recipient, sender, txn_sequence_no)
    else:
        sql_str = """
        insert into events_audit_txn
        (events_audit_id, height, time, 
        txn_type, amount, token, 
        validator, hash, recipient, sender, txn_sequence_no)
        VALUES ('{0}', '{1}', '{2}', 
        '{3}', '{4}', '{5}', 
        '{6}', '{7}', '{8}', '{9}', '{10}')
        """.format(id, height, timestamp,
                   txn_type, amount, token,
                   validator, hash, recipient, sender, txn_sequence_no)

    database_service.execute_update(sql_str)
