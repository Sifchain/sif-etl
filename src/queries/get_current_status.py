from src.services.database import database_service


def get_current_status_query():
    sql_str = """
        select count(*) as num_rec, max(a.time) as last_updated, 'tokenprices' as service  
        from tokenprices a where a.time = (select max(time) from tokenprices)
        union all
        select count(*) as num_rec, max(time) as last_updated, 'events_'||type as service from events_audit
        where time > now() - interval '1 weeks'
        group by service
        union all
        select count(*) as num_rec, max(timestamp) as last_updated, 'tokenprices_cmc' as service from tokenprices_coinmarketcap tc 
        where tc.is_latest = true
        order by service
    """
    return database_service.execute_query(sql_str)
