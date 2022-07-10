import psycopg2
import psycopg2.extras

from src.services.config import config_service


class DatabaseService:
    def __init__(self) -> None:
        self.connection = self.get_conn()
        self.cursor = self.get_cursor()
        self.dict_cursor = self.get_dict_cursor()

    def get_conn(self):
        self.connection = psycopg2.connect(
            database=config_service.pg_config["database"],
            user=config_service.pg_config["user"],
            password=config_service.pg_config["password"],
            host=config_service.pg_config["host"],
            port=config_service.pg_config["port"],
        )
        return self.connection

    def get_dict_cursor(self):
        self.connection = self.get_conn()
        self.connection.autocommit = True
        return self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_cursor(self):
        self.connection = self.get_conn()
        self.connection.autocommit = True
        return self.connection.cursor()

    def execute_scalar(self, sql_str):
        try:
            self.cursor.execute(sql_str)
        except Exception as e:
            print(e)
            self.cursor = self.get_cursor()
            self.cursor.execute(sql_str)
        record = self.cursor.fetchall()[0][0]
        return record

    def execute_query(self, sql_str):
        try:
            self.dict_cursor.execute(sql_str)
        except Exception as e:
            print(e)
            self.dict_cursor = self.get_dict_cursor()
            self.dict_cursor.execute(sql_str)
        ans = self.dict_cursor.fetchall()
        dict_result = []
        for row in ans:
            dict_result.append(dict(row))
        return dict_result

    def execute_update(self, sql_str):
        try:
            self.cursor.execute(sql_str)
        except psycopg2.InterfaceError as e:
            print(e)
            self.cursor = self.get_cursor()
            self.cursor.execute(sql_str)
        self.connection.commit()


database_service = DatabaseService()
