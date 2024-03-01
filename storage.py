import json
import sqlite3


class Database:
    def __init__(self, db_name="data.sqlite3"):
        self.db_name = db_name
        self._connection = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(self.db_name)
            except sqlite3.Error as e:
                raise RuntimeError(f"Failed to connect to database: {e}")
        return self._connection

    def execute(self, query, params=None):
        with self.connect() as conn:
            try:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Failed to execute query: {e}")

    def executemany(self, sql, values):
        with self.connect() as conn:
            try:
                cursor = conn.cursor()
                cursor.executemany(sql, values)
                conn.commit()
                return cursor
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Failed to execute query: {e}")


class FileStorage:
    def __init__(self, file_name="data.json"):
        self.file_name = file_name

    def write(self, data):
        with open(self.file_name, "a") as file:
            file.write(data)

    def read(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_name}")
