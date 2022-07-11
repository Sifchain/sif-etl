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


def export_token_volumes(_output_path: str) -> str:
    _start_date = datetime.date(2021, 1, 1)
    _end_date = datetime.date.today()
    return query_to_csv(_start_date, _end_date, _output_path, "tokenvolumes")


def export_token_prices(_output_path: str) -> str:
    _start_date = datetime.date(2021, 1, 1)
    _end_date = datetime.date.today()
    return query_to_csv(_start_date, _end_date, _output_path, "tokenprices")


def export_token_registry(_output_path: str) -> str:
    _start_date = datetime.date(2021, 1, 1)
    _end_date = datetime.date.today()
    return query_to_csv(
        _start_date, _end_date, _output_path, "token_registry", "modified"
    )


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
    if os.path.exists(file_path) and file_path:
        head, tail = os.path.split(file_path)
        with zipfile.ZipFile(
            file_path.replace(".csv", ".zip"), "w", zipfile.ZIP_DEFLATED
        ) as archive:
            archive.write(file_path, tail)
        os.remove(file_path)
    else:
        logger.info(f"File {file_path} doesn't exists.")


def export_history(_output_path: str):
    start_export_date = datetime.date(2021, 2, 8)
    end_export_date = datetime.date(2022, 7, 1)

    # tokenregistry
    token_registry_export = export_token_registry(_output_path)
    zip_csv(token_registry_export)

    # token_prices
    token_prices_export = export_token_prices(_output_path)
    zip_csv(token_prices_export)

    # token_volumes
    token_volumes_export = export_token_volumes(_output_path)
    zip_csv(token_volumes_export)

    # event_audit
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
            # event audit
            events_audit_output = export_events_audit(
                start_export_date, weekly_end_date, _output_path
            )
            zip_csv(events_audit_output)
            logger.info("Exporting completed successfully")

            start_export_date = weekly_end_date
        except Exception as e:
            logger.info(f"processing error: {e}")
            continue


def weekly_tables_export(_output_path: str):
    start_export_date = datetime.date.today()
    delta = datetime.timedelta(days=7)
    weekly_end_date = start_export_date - delta
    logger.info(f"Exporting data range from {start_export_date} to {weekly_end_date}")
    try:
        # event audit table
        events_audit_output = export_events_audit(
            start_export_date, weekly_end_date, output_path
        )
        zip_csv(events_audit_output)

        # token_prices
        token_prices_export = export_token_prices(_output_path)
        zip_csv(token_prices_export)

        # token_volumes
        token_volumes_export = export_token_volumes(_output_path)
        zip_csv(token_volumes_export)

        # token registry table
        token_registry_export = export_token_registry(_output_path)
        zip_csv(token_registry_export)

        logger.info("Exporting completed successfully")
    except Exception as e:
        logger.info(f"processing error: {e}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No command has been passed")
    elif len(sys.argv) <= 2:
        print("No output path has been passed")
    elif sys.argv[1] == "weekly":
        output_path = sys.argv[2]
        weekly_tables_export(output_path)
        # weekly output or history output
    elif sys.argv[1] == "history":
        output_path = sys.argv[2]
        export_history(output_path)
