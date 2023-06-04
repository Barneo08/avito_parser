import sqlite3 as sq
import pandas as pd

class MyDatabase:
    db_location = os.path.join("src", "query_cache.db")

    def __init__(self):
        self.db = sq.connect(Database.db_location)
        self.cur = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS query_cache(
            ad_id BIGINT NOT NULL PRIMARY KEY,
            date_public DATETIME,
            views INT,
            price TEXT,
            name TEXT,
            address TEXT,
            descriptions TEXT,
            url TEXT,
            city TEXT,
            request TEXT,
            is_closed INT,
            add_time DATETIME,
            update_time DATETIME
        )""")
        self.db.commit()

    def execute(self, query):
        self.cur.execute(query)
        self.db.commit()

    def close(self):
        self.db.close()