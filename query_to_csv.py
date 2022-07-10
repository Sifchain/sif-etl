import datetime
import logging
import os
import sys
import zipfile
import psycopg2
from src.services.database import database_service

from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(message)s")
logger = setup_logger_util("query_to_csv.py", formatter)


def export_events_audit(
    _start_date: datetime.date, _end_date: datetime.date, _output_path: str
) -> str:
    return query_to_csv(_start_date, _end_date, _output_path, "events_audit")


def query_to_csv(
    _start_date: datetime.date,
    _end_date: datetime.date,
    _output_path: str,
    table: str,
    time_column: str = "time",
) -> str:
    file_name = f"/{table}_{_start_date}.csv"
    path = _output_path + file_name
    sql_str = f"""
    select * 
    from {table} 
    where {time_column} >= to_timestamp('{_start_date}','YYYY-MM-dd') 
    and {time_column} < to_timestamp('{_end_date}','YYYY-MM-dd') 
    """
    conn = database_service.get_conn()
    db_cursor = conn.cursor()
    output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql_str)
    try:
        with open(path, "w") as f_output:
            db_cursor.copy_expert(output, f_output)
    except psycopg2.Error as err:
        print(err)
    db_cursor.close()
    conn.close()
    return path


def zip_csv(file_path: str) -> None:
    if os.path.exists(file_path) or file_path is None:
        head, tail = os.path.split(file_path)
        with zipfile.ZipFile(file_path.replace(".csv", ".zip"), mode="w") as archive:
            archive.write(file_path, tail)
        os.remove(file_path)
    else:
        logger.info(f"File {file_path} doesn't exists.")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("please provide a output path.")
    else:
        output_path = sys.argv[1]
        start_export_date = datetime.date(2021, 6, 1)
        end_export_date = datetime.date(2021, 9, 1)

        delta = datetime.timedelta(days=7)
        while start_export_date < end_export_date:
            try:
                weekly_end_date = start_export_date + delta
                if weekly_end_date.month != start_export_date.month:
                    weekly_end_date = datetime.date(
                        weekly_end_date.year, weekly_end_date.month, 1
                    )
                # data included in output file doesn't cross two month
                logger.info(
                    f"Exporting data range from {start_export_date} to {weekly_end_date}"
                )
                events_audit_output = export_events_audit(
                    start_export_date, weekly_end_date, output_path
                )
                logger.info("Exporting completed successfully")
                zip_csv(events_audit_output)
                start_export_date = weekly_end_date
            except Exception as e:
                logger.info(f"processing error: {e}")
                continue
