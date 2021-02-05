# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import time
import datetime
import asyncio
import get_objects
import db

def start():
    list_of_objects = get_objects.get_objects_receivers("active_only")
    
    loopy(list_of_objects)

def loopy(list_of_objects):
    flag = True
    while flag:
        start = time.time()

        ioloop = asyncio.get_event_loop()

        tasks = [ioloop.create_task(get(i)) for i in list_of_objects]
        
        wait_tasks = asyncio.wait(tasks)
        ioloop.run_until_complete(wait_tasks)
        ioloop.close()
            
        print(tic(start))
        
        # writing results in db
        save_results(list_of_objects) 

        flag = False
        
async def get(i):
    #print(i)
    try:
        await i.get_parameters()
    except:
        i.color = "gray"
    if i.color != "gray":
        # Looking types and make check if needed
        if i.c_n == "0" or i.eb_no == "0" or i.l_m == "0":
            i.color = "red"
        elif float(i.c_n) <= 8.0 or float(i.eb_no) <=6.0:
            i.color = "yellow"
        else:
            i.color = "green"
    i.time = datetime.datetime.now().strftime("%H:%M")

def tic(start):
    return 'at %1.1f seconds' % (time.time() - start)

def print_obj(l):
    for i in l:
        print(i.c_n)

def save_results(list_of_objects):
    for i in list_of_objects:
        with db.DB() as curs:
            curs.execute('UPDATE receivers SET time=:time, c_n=:c_n, eb_no=:eb_no, l_m=:l_m  WHERE ip=:ip AND port=:port',{"ip":i.ip, "port":i.port, "time":i.time, "c_n":i.c_n, "eb_no":i.eb_no, "l_m":i.l_m})

if __name__ == "__main__":
    start()
