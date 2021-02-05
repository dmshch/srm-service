# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.
# Making and getting objects

from pathlib import *
import sqlite3
import db

#from . import load_data_from_db

# sync
#from receivers import proview2962_telnet.py
#from receivers import proview7000_telnet.py
#from receivers import proview7100s_ssh.py
#from receivers import proview7100mold_ssh.py

# async
from receivers import proview2962_telnet_async
from receivers import proview7000_telnet_async
from receivers import proview7100s_ssh_async
from receivers import proview7100mold_ssh_async
from receivers import proview8130_http_async
from receivers import proview7100mnew_http_async

def get_objects_receivers(flag):

    list_of_receivers = load_all_receivers()

    list_of_objects = []
    for i in list_of_receivers:
        
        ip, model, satellite, login, password, port, state, time, c_n, eb_no, l_m = i

        if  flag == "active_only" and state != 0:
            list_of_objects.append(return_object(ip, model, satellite, login, password, port, state))
        if flag == "all":
            list_of_objects.append(return_object(ip, model, satellite, login, password, port, state))
            
    return list_of_objects

def return_object(ip, model, satellite, login, password, port, state):

    # getting default login and password, if they not set in receivers table
    if login == "" and password == "":
        login, password = get_login_and_password(model)

    if model == "proview2962":
        receiver = proview2962_telnet_async.ProView2962(ip, model, satellite, login, password, port, state)
    if model == "proview7000":
        receiver = proview7000_telnet_async.ProView7000(ip, model, satellite, login, password, port, state)
    if model == "proview7100s":
        receiver = proview7100s_ssh_async.ProView7100s(ip, model, satellite, login, password, port, state)
    if model == "proview7100mold":
        receiver = proview7100mold_ssh_async.ProView7100mold(ip, model, satellite, login, password, port, state)
    if model == "proview8130":
        receiver = proview8130_http_async.ProView8130(ip, model, satellite, login, password, port, state)
    if model == "proview7100mnew":
        receiver = proview7100mnew_http_async.ProView7100mnew(ip, model, satellite, login, password, port, state)
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
