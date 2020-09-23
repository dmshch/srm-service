# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import sqlite3
from pathlib import *

# delete data from sqlite

def delete_data(ip, port):
    status = ""
    conn = sqlite3.connect(str(Path.cwd()) + "/servmoncode/servermon.db")
    curs = conn.cursor()
    curs.execute('DELETE FROM receivers WHERE ip=:ip AND port=:port',{"ip":ip, "port":port})
    status = "IP address and port have been removed"
    conn.commit()
    curs.close()
    conn.close()
    return status
