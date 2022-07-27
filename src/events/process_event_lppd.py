from src.mutations.create_events import create_event_lddp_rewards_dist_mutation
from src.utils.decode_attributes import decode_attributes_util


def process_event_lppd_distribution(event_type, attrs, height, timestamp) -> None:
    result = decode_attributes_util(attrs)
    ld_recipient_addr = result.get("recipient")
    ld_total_amount = result.get("total_amount")
    ld_amount = result.get("amounts")
    create_event_lddp_rewards_dist_mutation(height, event_type, timestamp, ld_recipient_addr,
                                            ld_total_amount, ld_amount)


def generate_event_lppd_distribution(event_type, attrs, height, timestamp) -> str:
    result = decode_attributes_util(attrs)
    ld_recipient_addr = result.get("recipient")
    ld_total_amount = result.get("total_amount")
    ld_amount = result.get("amounts")
    sql_str = f"""        
        select {height},'{event_type}',cast('{timestamp}' as timestamp)
        ,'{ld_recipient_addr}',{ld_total_amount},cast('{ld_amount}' as jsonb)    
        """
    return sql_str
