import datetime
import sys
import zipfile

import psycopg2
from src.services.database import database_service


def export_events_audit(_start_date: datetime.date, _end_date: datetime.date, _output_path: str) -> None:
    query_to_csv(_start_date, _end_date, _output_path, "events_audit")


def query_to_csv(_start_date: datetime.date, _end_date: datetime.date, _output_path: str, table: str,
                 time_column: str = "time") -> None:
    file_name = f"/{table}_{_start_date}.csv"
    path = _output_path + file_name
    sql_str = f"""
    select * 
    from {table} 
    where {time_column} >= to_timestamp('{_start_date}','YYYY-MM-dd') 
    and {time_column} < to_timestamp('{_end_date}','YYYY-MM-dd') 
    """
    print(sql_str, path)
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


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("please provide a output path.")
    else:
        output_path = sys.argv[1]
        start_export_date = datetime.date(2021, 4, 1)
        end_export_date = datetime.date(2021, 4, 1)

        with zipfile.ZipFile("/media/sf_shared/hello.zip", mode="w") as archive:
            archive.write("/media/sf_shared/sifchain-pem.csv")

        delta = datetime.timedelta(days=7)
        while start_export_date < end_export_date:
            weekly_end_date = start_export_date + delta
            if weekly_end_date.month != start_export_date.month:
                weekly_end_date = datetime.date(weekly_end_date.year, weekly_end_date.month, 1)
            # don't cross two month
            print(start_export_date, weekly_end_date)
            export_events_audit(start_export_date, weekly_end_date, output_path)
            start_export_date = weekly_end_date

# start_export_date = datetime.date(2022, 5, 8)
# export_table_to_csv(start_export_date, "/db/scripts", "events_audit")
