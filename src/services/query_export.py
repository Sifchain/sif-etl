import datetime

import psycopg2
from src.services.database import database_service


def export_table_to_csv(start_date: datetime.date, file_path: str, table: str, time_column: str = "time"):
    file_name = f"/{table}_{start_date}.csv"
    path = file_path + file_name
    end_date = start_date + datetime.timedelta(days=7)
    sql_str = f"""
    select * 
    from {table} 
    where {time_column} >= to_timestamp('{start_date}','YYYY-MM-dd') 
    and {time_column} < to_timestamp('{end_date}','YYYY-MM-dd') 
    """
    # print(sql_str, path)
    conn = database_service.get_conn()
    db_cursor = conn.cursor()
    output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql_str)
    try:
        with open(path, 'w') as f_output:
            db_cursor.copy_expert(output, f_output)
    except psycopg2.Error as e:
        print(e)

    db_cursor.close()
    conn.close()
    print("Export completed successfully")


start_export_date = datetime.date(2022, 5, 8)
export_table_to_csv(start_export_date, "/home/sxiao/src/sif-etl/db/scripts", "events_audit")
