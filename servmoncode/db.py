# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

# class wrapper for working with database

import sqlite3
from pathlib import *

if __name__ == "__main__":
    path_to_db = "servermon.db"
else:
    #path_to_db = str(Path.cwd()) + "servermon.db"
    path_to_db = "servermon.db"

class DB:

    def __init__(self):
        self.file = path_to_db

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.curs = self.conn.cursor()
        return self.curs

    def __exit__(self, *args):
        self.conn.commit()
        self.curs.close()
        self.conn.close()
        #print("END1")

if __name__ == "__main__":
    with DB() as curs:
        curs.execute('SELECT * FROM receivers')
        rows = curs.fetchall()
        for res in rows:
            print(res)
    #print("END2")
