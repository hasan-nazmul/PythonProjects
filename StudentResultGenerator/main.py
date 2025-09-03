import time
import tkinter
import datetime
import csv
import sqlite3
import os
import uuid
from dataclasses import dataclass


def adapt_datetime_iso(dt_obj):
    """Adapts a datetime.datetime object to an ISO 8601 formatted string."""
    return dt_obj.isoformat()

def convert_timestamp_iso(ts_bytes):
    """Converts an ISO 8601 formatted string (as bytes) to a datetime.datetime object."""
    return datetime.datetime.fromisoformat(ts_bytes.decode('utf-8'))

# 3. Register the new functions with the sqlite3 library
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_converter("timestamp", convert_timestamp_iso)


class PathError(Exception):
    def __init__(self, msg:str):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileError(Exception):
    def __init__(self, msg:str):
        self.msg = msg

    def __str__(self):
        return self.msg


class Database:
    def __init__(self, db_path:str, db_name='my.db'):
        if os.path.isdir(db_path):
            self.db_dir, self.db_name = db_path, db_name
        elif os.path.isfile(db_path):
            self.db_dir, self.db_name = os.path.split(db_path)
        else:
            raise PathError(f"Your provided path: {db_path} doesn't exist!")

        # Initialize SQLite connection
        self._connection = sqlite3.connect(os.path.join(self.db_dir, self.db_name))
        self._cursor = self._connection.cursor()

    @property
    def db_dir(self):
        return self._db_dir

    @db_dir.setter
    def db_dir(self, db_dir):
        self._db_dir = db_dir

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        if not db_name.lower().endswith('.db'):
            raise FileError("Provided File Path is not a .db file!")
        self._db_name = db_name

    def execute(self, query, params=None):
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            self._connection.commit()
            return self._cursor.fetchall()
        except sqlite3.Error as e:
            print(f'There was an error: {e}')
            return None

    def executemany(self, query, params_list):
        try:
            self._cursor.executemany(query, params_list)
            self._connection.commit()
            return self._cursor.rowcount
        except sqlite3.Error as e:
            print(f'There was an error: {e}')
            return None

    def write(self, table_name: str, obj):
        columns = tuple(obj.__dict__.keys())
        values = tuple(obj.__dict__.values())

        column_names = ', '.join(columns)
        placeholders = ', '.join([f':{col}' for col in columns])

        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        self.execute(query, obj.__dict__)

    def stop(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

@dataclass
class Entry:
    def __init__(self, description:str, category:str, amount:int):
        self.e_id = str(uuid.uuid4())
        self.e_date = datetime.datetime.now()
        self.e_desc = description
        self.e_cat = category
        self.e_amount = amount

    def __str__(self):
        date_str = self.e_date.strftime('%d %B, %A %Y, %H:%M:%S')
        return (f'ID: {self.e_id}\n'
                f'Date: {date_str}\n'
                f'Description: {self.e_desc}\n'
                f'Category: {self.e_cat}\n'
                f'Amount: {self.e_amount}')


class DBtoCSV(csv.DictWriter):
    def __init__(self, db:Database, table_name:str):
        self.rows = db.execute(f'select * from {table_name}')
        self.headers = [col[1] for col in db.execute(f'pragma table_info({table_name})')]
        self.dicts = []

    def write(self):
        for row in self.rows:
            d = {}
            for i in range(len(self.headers)):
                d[self.headers[i]] = row[i]
            self.dicts.append(d)
        with open(f'transaction{round(time.time())*1000}.csv', 'w', newline='') as new_csv:
            super().__init__(new_csv, fieldnames=self.headers, delimiter=',')
            super().writeheader()
            super().writerows(self.dicts)


def main():
    pass


if __name__ == '__main__':
    main()