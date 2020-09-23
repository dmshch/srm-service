# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from pathlib import *
import sqlite3

#edit settings from web gui

# load all settings as dict 
def get_settings():
    settings, receiver_authentication, user_authentication = dict(), dict(),dict()
    conn = sqlite3.connect(str(Path.cwd()) + "/servmoncode/servermon.db")
    curs = conn.cursor()
    curs.execute('SELECT * FROM receivers WHERE ip=:ip AND port=:port',{"ip":ip, "port":port})
    row_of_receivers = curs.fetchall()
    tuple_of_keys = ('ip', 'model', 'satellite', 'login', 'password', 'port', 'state')
    # receiver is dict -> keys: ip, model, satellite, login, password, port, state
    for res in row_of_receivers:
        receiver = dict(zip(tuple_of_keys, res))
    curs.close()
    conn.close()
    return settings, receiver_authentication, user_authentication


