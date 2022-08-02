# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import sqlalchemy as sa 
import json
import pathlib
from datetime import datetime
from datetime import timedelta
import uuid

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

                # Need to rename in classes -> cc_delta

                ip, port, time, c_n, eb_no, l_m, service, cc = i.ip, i.port, i.time, i.c_n, i.eb_no, i.l_m, i.service, i.cc

                try:
                    c_n = round(float(c_n), 2)
                    eb_no = round(float(eb_no), 2)
                    l_m = round(float(l_m), 2)
                except:
                    pass
                
                # Get old value for cc
                query = sa.select([receivers.columns.cc]).where(receivers.columns.ip == ip).where(receivers.columns.port == port)
                ResultProxy = conn.execute(query)
                ResultSet = ResultProxy.first()
                old_cc = ResultSet[0]
                
                # Count and save
                cc = cc.strip()
                try:
                    float(cc)
                except:
                    cc = "parsing error"                

                try:
                    float(old_cc)
                except:
                    old_cc = "parsing error"
                    
                cc_delta = "n/a"
                
                if old_cc == "parsing error" or cc == "parsing error":
                    cc_delta = 0
                elif old_cc != "parsing error" and cc != "parsing error":
                    cc_delta = float(cc) - float(old_cc)
                
                #print(f"cc - {cc}")
                #print(f"old_cc - {old_cc}")
                #print(f"cc_delta - {cc_delta}")
                
                query = sa.update(receivers).values(time = time, c_n = c_n, eb_no = eb_no, l_m = l_m, service = service, cc_delta = cc_delta, cc = cc)
                query = query.where(receivers.columns.ip == ip).where(receivers.columns.port == port)
                results = conn.execute(query)

                # Save new statistics
                #  ip | port | time | c_n | eb_no | l_m
                guid = str(uuid.uuid4())
                try:
                    date_time = datetime.strptime(time, '%Y %b %d %H:%M').isoformat()
                    query = sa.insert(statistics).values(ip = ip, port = port, c_n = c_n, eb_no = eb_no, l_m = l_m, date_time = date_time, guid = guid)
                    ResultProxy = conn.execute(query)
                except:
                    continue

            # Delete old statistics
            current_time = datetime.now()
            delta = timedelta(days = 31)
            limit = (current_time - delta).isoformat()
            query = sa.delete(statistics).where(statistics.columns.date_time <= limit)
            conn.execute(query)
            conn.close()

        self.engine.dispose()
