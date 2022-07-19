import datetime
import logging
import os
import sys
import zipfile
import boto3
import psycopg2

from src.services.database import database_service
from src.utils.setup_logger import setup_logger_util

formatter = logging.Formatter("%(message)s")
logger = setup_logger_util("query_to_csv.py", formatter)

BUCKET_NAME = 'timescalebackup'
AWS_PROFILE = 'common'


def upload_file_to_s3(path: str, folder_name: str = None) -> None:
    if os.path.exists(path) and path:
        session = boto3.Session(profile_name=AWS_PROFILE)
        s3 = session.client('s3')
        bucket_name = BUCKET_NAME
        object_name = os.path.basename(path)
        if folder_name:
            object_name = f"{folder_name}/{os.path.basename(path)}"
        s3.upload_file(path, bucket_name, object_name)
        os.remove(path)
    else:
        logger.info("There is nothing to upload")


def export_from_query(sql_str: str, _path: str) -> str:
    conn = database_service.get_conn()
    db_cursor = conn.cursor()
    output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sql_str)
    try:
        with open(_path, "w") as f_output:
            db_cursor.copy_expert(output, f_output)
    except psycopg2.Error as err:
        print(err)
    db_cursor.close()
    conn.close()
    return _path


def export_events_audit(
        _start_date: datetime.date, _end_date: datetime.date, _output_path: str
) -> str:
    return query_to_csv(_start_date, _end_date, _output_path, "events_audit")


def export_token_volumes(
        _start_date: datetime.date, _end_date: datetime.date, _output_path: str
) -> str:
    return query_to_csv(_start_date, _end_date, _output_path, "tokenvolumes")


def export_token_prices(
        _start_date: datetime.date, _end_date: datetime.date, _output_path: str
) -> str:
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
    _file_name = f"/{table}_{_start_date}.csv"
    _path = _output_path + _file_name
    sql_str = f"""
    select * 
    from {table} 
    where {time_column} >= to_timestamp('{_start_date}','YYYY-MM-dd') 
    and {time_column} < to_timestamp('{_end_date}','YYYY-MM-dd') 
    """
    return export_from_query(sql_str, _path)


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


def historical_tables_export(_output_path: str) -> None:
    start_date = datetime.date(2022, 7, 1)
    end_date = datetime.date.today()

    zip_token_registry_and_upload(_output_path)

    # token_prices & token_volumes monthly export
    delta_month = datetime.timedelta(days=31)
    while start_date < end_date:
        try:
            _end_date = start_date + delta_month
            if _end_date.month != start_date.month:
                _end_date = datetime.date(_end_date.year, _end_date.month, 1)

            zip_token_prices_and_upload(_end_date, _output_path, start_date)

            zip_token_volumes_and_upload(_end_date, _output_path, start_date)

            start_date = _end_date
        except Exception as e:
            logger.info(f"processing error: {e}")
            continue

    # event_audit
    start_date = datetime.date(2022, 7, 1)
    end_date = datetime.date.today()
    delta = datetime.timedelta(days=7)
    while start_date < end_date:
        try:
            weekly_end_date = start_date + delta
            if weekly_end_date.month != start_date.month:
                weekly_end_date = datetime.date(
                    weekly_end_date.year, weekly_end_date.month, 1
                )
            # data included in output file doesn't cross two month
            logger.info(
                f"Exporting event_audit from {start_date} to {weekly_end_date}"
            )
            # event audit
            zip_events_audit_and_upload(_output_path, start_date, weekly_end_date)

            start_date = weekly_end_date
        except Exception as e:
            logger.info(f"processing error: {e}")
            continue


def zip_events_audit_and_upload(_output_path, _start_date, _end_date):
    events_audit_output = export_events_audit(
        _start_date, _end_date, _output_path
    )
    zip_csv(events_audit_output)
    zipped_events_audit_output = events_audit_output.replace("csv", "zip")
    upload_file_to_s3(zipped_events_audit_output, "events_audit")
    logger.info(f"Export and upload file {zipped_events_audit_output} successfully for events audit")


def zip_token_volumes_and_upload(_end_date, _output_path, _start_date):
    # token_volumes
    token_volumes_export = export_token_volumes(
        _start_date, _end_date, _output_path
    )
    zip_csv(token_volumes_export)
    zipped_token_volumes_export = token_volumes_export.replace(".csv", ".zip")
    upload_file_to_s3(zipped_token_volumes_export, "tokenvolumes")
    logger.info(f"Export and upload file {zipped_token_volumes_export} successfully for token volumes")


def zip_token_registry_and_upload(_output_path):
    # token registry
    token_registry_export = export_token_registry(_output_path)
    zip_csv(token_registry_export)
    zipped_token_registry_export = token_registry_export.replace(".csv", ".zip")
    upload_file_to_s3(zipped_token_registry_export)
    logger.info(f"Export and upload file {zipped_token_registry_export} successfully for token registry")


def zip_token_prices_and_upload(_end_date, _output_path, _start_date) -> None:
    # token_prices
    token_prices_export = export_token_prices(
        _start_date, _end_date, _output_path
    )
    zip_csv(token_prices_export)
    zipped_token_prices_export = token_prices_export.replace("csv", "zip")
    upload_file_to_s3(zipped_token_prices_export, "tokenprices")
    logger.info(f"Export and upload file {zipped_token_prices_export} successfully for token prices")


def latest_tables_export(_output_path: str) -> None:
    _today = datetime.date.today()
    _export_start_date = datetime.date(_today.year, _today.month, _today.day // 7 * 7 + 1)
    logger.info(f"Exporting data range from {_export_start_date} to {_today}")
    try:
        # event audit table
        zip_events_audit_and_upload(output_path, _export_start_date, _today)

        # export month data for token_prices & token_volumes
        _start_date = datetime.date(_today.year, _today.month, 1)

        # token_prices
        zip_token_prices_and_upload(_today, _output_path, _start_date)

        # token_volumes
        zip_token_volumes_and_upload(_today, _output_path, _start_date)

        # token registry table
        zip_token_registry_and_upload(_output_path)

        logger.info("Exporting completed successfully")
    except Exception as e:
        logger.info(f"processing error: {e}")


if __name__ == "__main__":
    # latest or historical output
    # example 1: python query_to_csv.py latest /media/sf_shared
    # example 2: python query_to_csv.py historical /media/sf_shared
    # example 3: python query_to_csv.py query /media/sf_shared
    if len(sys.argv) <= 1:
        print("No command has been passed")
    elif len(sys.argv) <= 2:
        print("No output path has been passed")
    elif sys.argv[1] == "latest":
        output_path = sys.argv[2]
        latest_tables_export(output_path)
    elif sys.argv[1] == "historical":
        output_path = sys.argv[2]
        historical_tables_export(output_path)
    elif sys.argv[1] == "query":
        output_path = sys.argv[2]
        query = "select * from events_audit where type = 'swap_successful' and time > '2022-03-01'"
        file_name = f"/export_{datetime.date.today()}.csv"
        path = output_path + file_name
        output_from_query = export_from_query(query, path)
        zip_csv(output_from_query)
