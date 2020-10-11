 # Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from pathlib import *
import sqlite3
from servmoncode import db

#make and get object

#from . import load_data_from_db
from .receivers import proview2962
from .receivers import proview7000
from .receivers import proview7100s
from .receivers import proview7100mold

def get_objects_receivers(flag):

    list_of_receivers = load_all_receivers()

    list_of_objects = []
    for i in list_of_receivers:
        
        ip, model, satellite, login, password, port, state = i

        if  flag == "active_only" and state != 0:
            list_of_objects.append(return_object(ip, model, satellite, login, password, port, state))
        if flag == "all":
            list_of_objects.append(return_object(ip, model, satellite, login, password, port, state))
            
    return list_of_objects

def return_object(ip, model, satellite, login, password, port, state):
    if login == "" and password == "":
        login, password = get_login_and_password(model)
    if model == "proview2962":
        receiver = proview2962.ProView2962(ip, model, satellite, login, password, port, state)
    if model == "proview7000":
        receiver = proview7000.ProView7000(ip, model, satellite, login, password, port, state)
    if model == "proview7100s":
        receiver = proview7100s.ProView7100s(ip, model, satellite, login, password, port, state)
    if model == "proview7100mold":
        receiver = proview7100mold.ProView7100mold(ip, model, satellite, login, password, port, state)
    return receiver

def get_login_and_password(model):
    with db.DB() as curs:
        curs.execute('SELECT login,password FROM receiver_authentication WHERE model=:model',{"model":model})
        rows = curs.fetchall()
        for i in rows:
            login, password = i
    return login, password

# load all receivers from sqlite
def load_all_receivers():
    with db.DB() as curs:
        curs.execute('SELECT * FROM receivers')
        rows = curs.fetchall()
    return rows
