import sqlite3
from contextlib import closing

import os
import sys

db_dir = os.path.dirname(os.path.dirname(os.path.abspath(''))) + '/db/my_database.db3'

class Database:
    def __init__(self, db_path=db_dir):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql, params=()):
        with closing(self.connect()) as conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()

    def execute_script(self, script):
        with closing(self.connect()) as conn:
            with conn:
                cursor = conn.cursor()
                cursor.executescript(script)