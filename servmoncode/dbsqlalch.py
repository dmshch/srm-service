# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import sqlalchemy as sa
import json
import pathlib

def get_engine():
    path = str(pathlib.Path().absolute()) + "/settings.json"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Failed to load settings. Check the correctness of the settings file 'settings.json'.")
    path = data["dialect"] + "+" + data["driver"] + "://" + data["user"] + ":" + data["password"] + "@" + data["host"] + ":" + data["port"] + "/" + data["dbname"]
    engine = sa.create_engine(path)
    return engine

def load_all_receivers():
    with get_engine().connect() as conn:
    #with DB() as conn:
        rows = conn.execute('SELECT * FROM receivers WHERE state = True')
        return rows

def get_login_and_password(model):
    with get_engine().connect() as conn:
        postgresql_select_query = 'SELECT login,password FROM receiver_authentication WHERE model= %s'
        rows = conn.execute(postgresql_select_query, (model, ))
        for row in rows:
            login, password = row
    return login, password

def save(list_of_objects):
    with get_engine().connect() as conn:
        for i in list_of_objects:
            ip, port, time, c_n, eb_no, l_m = i.ip, i.port, i.time, i.c_n, i.eb_no, i.l_m
            postgresql_update_query = 'UPDATE receivers SET time = %s, c_n = %s, eb_no = %s, l_m = %s WHERE ip = %s AND port = %s'
            rows = conn.execute(postgresql_update_query, (time, c_n, eb_no, l_m, ip, port, ))
