import sqlite3

from storage_services.databases.utilities import (
    AtomicAction,
    split_statements,
)

from .configuration import PREREQUISITE_SQL_FILE


class SqliteClient:
    def __init__(self, database):
        self.database = database

    def get_service_connection(self):
        conn = sqlite3.connect(fr"{self.database}")
        return conn

    def get_service_cursor(self):
        return self.service_connection.cursor()

    def run_prerequisites(self, atomic=False):
        prerequisite_file = PREREQUISITE_SQL_FILE['location']

        with open(prerequisite_file) as f_ptr:
            f_contents = f_ptr.read()

        stmnt_list = split_statements(f_contents)
        with AtomicAction(self, atomic) as conn:
            for statement in stmnt_list:
                print("Executing ... ")
                print("--"*(80))
                print(statement)
                conn.execute(statement)

    def create_table(self, sql_statement, atomic=True):
        with AtomicAction(self, atomic) as conn:
            try:
                conn.execute(sql_statement)
            except sqlite3.Error as err:
                print(f"Exception raised while creating tables: {err}")

    def create_table_in_bulk(self, sql_statements, atomic=True):
        with AtomicAction(self, atomic) as conn:
            try:
                conn.executemany(sql_statements)
            except sqlite3.Error as err:
                print(f"Exception raised while creating tables in bulk: {err}")

    def query_result(self, sql_statement, records_count=10):
        connection = self.get_service_connection()
        try:
            result = connection.execute(sql_statement)
        except sqlite3.Error as err:
            result = None
            print(f"Exception raised while fetching result: {err}")
        finally:
            if result:
                result = result.fetchmany(records_count)
            connection.close()

        return result

    def insert_row(self, sql_statement, parameters=(), atomic=True):
        with AtomicAction(self, atomic) as conn:
            try:
                if parameters:
                    conn.execute(sql_statement, parameters)
                else:
                    conn.execute(sql_statement)
            except sqlite3.Error as err:
                print(f"Exception raised while inserting rows: {err}")

    def insert_rows_in_bulk(self, sql_statements, atomic=True):
        with AtomicAction(self, atomic) as conn:
            try:
                conn.executemany(sql_statements)
            except sqlite3.Error as err:
                print(f"Exception raised while inserting rows in bulk: {err}")

