from services import database_service


def update_slack_sent_mutation(message_type, recipient, message=None):
    if message is None:
        sql_str = """
            with notif as (select id from notifications where notification_type= '{0}' and destination='{1}' and notification_channel = 'slack')
            insert into notifications_status
            (notification_id, sent_on)
            select id, now()
            from notif
        """.format(message_type, recipient)
    else:
        sql_str = """
            with notif as (select id from notifications where notification_type= '{0}' and destination='{1}' and notification_channel = 'slack')
            insert into notifications_status
            (notification_id, sent_on, message)
            select id, now(), '{2}'
            from notif
        """.format(message_type, recipient, message)

    database_service.execute_update(sql_str)
