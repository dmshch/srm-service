# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import sqlalchemy as sa
import json

class DB:

    def __init__(self):
        try:
            with open("servmoncode/settings.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            print("Failed to load settings. Check the correctness of the settings file 'servmoncode/settings.json'.")

        #self.path = dialect + "+" + driver + "://" + user+ ":" + password + "@" + host + ":" + port + "/" + dbname
        self.path = data["dialect"] + "+" + data["driver"] + "://" + data["user"] + ":" + data["password"] + "@" + data["host"] + ":" + data["port"] + "/" + data["dbname"]
        #print(self.path)

    def __enter__(self):
        self.conn = sa.create_engine(self.path)
        return self.conn

    def __exit__(self, *args):
        # ?
        pass

def load_all_receivers():
    with DB() as conn:
        rows = conn.execute('SELECT * FROM receivers')
        return rows

def get_login_and_password(model):
    with DB() as conn:
        postgresql_select_query = 'SELECT login,password FROM receiver_authentication WHERE model= %s'
        rows = conn.execute(postgresql_select_query, (model, ))
        #print(rows)
        for row in rows:
            login, password = row
    return login, password

def save(ip, port, time, c_n, eb_no, l_m):
    with DB() as conn:
        postgresql_update_query = 'UPDATE receivers SET time = %s, c_n = %s, eb_no = %s, l_m = %s WHERE ip = %s AND port = %s'
        rows = conn.execute(postgresql_update_query, (time, c_n, eb_no, l_m, ip, port, ))

if __name__ == "__main__":
    pass
