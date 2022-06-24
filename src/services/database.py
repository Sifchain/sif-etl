import psycopg2
import psycopg2.extras

from src.services.config import config_service


class DatabaseService:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            database=config_service.pg_config['database'],
            user=config_service.pg_config['user'],
            password=config_service.pg_config['password'],
            host=config_service.pg_config['host'],
            port=config_service.pg_config['port']
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    def execute_scalar(self, sql_str):
        self.cursor.execute(sql_str)
        record = self.cursor.fetchall()[0][0]
        return record

    def execute_query(self, sql_str):
        self.dict_cursor.execute(sql_str)
        ans = self.dict_cursor.fetchall()
        dict_result = []
        for row in ans:
            dict_result.append(dict(row))
        return dict_result

    def execute_update(self, sql_str):
        self.cursor.execute(sql_str)
        self.connection.commit()


database_service = DatabaseService()
