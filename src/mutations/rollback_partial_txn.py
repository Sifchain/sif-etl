from src.services.database import database_service


def rollback_partial_txn_mutation(event_id):
    sql_str = """
        DELETE from events_audit_txn
        WHERE events_audit_id = {0}
    """.format(event_id)
    database_service.execute_update(sql_str)
