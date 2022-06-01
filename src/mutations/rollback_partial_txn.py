from services.config import config_service
from services import database_service


def rollback_partial_txn_mutation(event_id):
    sql_str = """
        DELETE from {1}
        WHERE events_audit_id = {0}
    """.format(event_id, config_service.schema_config["EVENT_TXN_TABLE"])
    database_service.execute_update(sql_str)
