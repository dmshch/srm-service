# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import sqlalchemy as sa
import json
import pathlib
from datetime import datetime

class DB():
    engine = None
    def __init__(self):
        path = str(pathlib.Path().absolute()) + "/settings.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Failed to load settings. Check the correctness of the settings file 'settings.json'.")
        path = data["dialect"] + "+" + data["driver"] + "://" + data["user"] + ":" + data["password"] + "@" + data["host"] + ":" + data["port"] + "/" + data["dbname"]
        self.engine = sa.create_engine(path)

    def load_all_receivers(self):
        with self.engine.connect() as conn:
            metadata = sa.MetaData()
            receivers = sa.Table('receivers', metadata, autoload=True, autoload_with=conn)
            models = sa.Table('receiver_models', metadata, autoload=True, autoload_with=conn)

            query = sa.select([receivers.columns.guid,receivers.columns.ip, receivers.columns.port, models.columns.model, receivers.columns.satellite, models.columns.login, models.columns.password, receivers.columns.state, receivers.columns.c_n, receivers.columns.eb_no, receivers.columns.l_m, receivers.columns.time]).where(receivers.columns.state == "True")
            query = query.select_from(receivers.join(models, receivers.columns.model == models.columns.guid))
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
            rows = ResultSet
            conn.close()
        self.engine.dispose()
        return rows

    def get_login_and_password(self, model):
        with self.engine.connect() as conn:
            metadata = sa.MetaData()
            receiver_authentication = sa.Table('receiver_models', metadata, autoload=True, autoload_with=conn)
            query = sa.select([receiver_authentication.columns.login,receiver_authentication.columns.password]).where(receiver_authentication.columns.model == model)
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
            rows = ResultSet

            for row in rows:
                login, password = row
            conn.close()
        self.engine.dispose()
        return login, password

    def save(self, list_of_objects):
        with self.engine.connect() as conn:
            metadata = sa.MetaData()
            receivers = sa.Table('receivers', metadata, autoload=True, autoload_with=conn)
            statistics = sa.Table('statistics', metadata, autoload=True, autoload_with=conn)
            for i in list_of_objects:
                ip, port, time, c_n, eb_no, l_m, service = i.ip, i.port, i.time, i.c_n, i.eb_no, i.l_m, i.service
                query = sa.update(receivers).values(time = i.time, c_n = i.c_n, eb_no = i.eb_no, l_m = i.l_m, service = i.service)
                query = query.where(receivers.columns.ip == i.ip).where(receivers.columns.port == i.port)
                results = conn.execute(query)
                # Statistics
                #  ip | port | time | c_n | eb_no | l_m
                try:
                    date_time = datetime.strptime(time, '%Y %b %d %H:%M').isoformat()
                    query = sa.insert(statistics).values(ip = ip, port = port, c_n = c_n, eb_no = eb_no, l_m = l_m, date_time = date_time)
                    ResultProxy = conn.execute(query)
                except:
                    continue
            conn.close()
        self.engine.dispose()
