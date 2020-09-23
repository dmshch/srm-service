# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import time
import threading
import datetime

def start(list_of_objects):
    p = threading.Thread(target = loopy, args=(list_of_objects,))
    p.start()
        

def loopy(list_of_objects):
    flag = True
    while flag:
        for i in list_of_objects:
            t = datetime.datetime.now().strftime("%H:%M")
            i.time = t
            try:
                i.get_parameters()
            except:
                i.color = "gray"
                continue
            
            # Looking types and make check if needed
            if i.c_n == "0" or i.eb_no == "0" or i.l_m == "0":
                i.color = "red"
            elif float(i.c_n) <= 8.0 or float(i.eb_no) <=6.0:
                i.color = "yellow"
            else:
                i.color = "green"

        time.sleep(600)
