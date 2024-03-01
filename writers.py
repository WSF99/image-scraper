from abc import ABC, abstractstaticmethod
from datetime import datetime

from queries import CREATE_IMAGES_TABLE, INSERT_IMAGES
from storage import Database, FileStorage


class IWriter(ABC):
    @abstractstaticmethod
    def write(data):
        pass


class DatabaseWriter(IWriter):
    def __init__(self):
        self.db = Database()
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        self.table_name = f"img_{int(timestamp)}"
        self.db.execute(CREATE_IMAGES_TABLE(self.table_name))

    def write(self, data: list[str]):
        try:
            query = INSERT_IMAGES(self.table_name)
            if data:
                values = [(url,) for url in data]
                self.db.executemany(query, values)
        except Exception as e:
            print(f"Error writing to the database: {e}")


class FileWriter(IWriter):
    def __init__(self):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        self.file_name = f"img_{int(timestamp)}.txt"

    def write(self, data: list[str]):
        file_storage = FileStorage(self.file_name)
        formatted_data = "\n".join(data) + "\n"
        file_storage.write(formatted_data)
