import sqlite3
from db_assets.db_recipes import *


class WebsiteDB:

    def __init__(self, db_name, tables=None):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        if tables is not None:
            self.tables = tables
        else:
            self.tables = []
        self.scan_for_tables()

    def scan_for_tables(self):
        # if selected tables don't exist we recreate them in a current db instance/record

        for table in self.tables:
            self.cursor.execute(table)
            self.conn.commit()
