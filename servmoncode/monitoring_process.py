# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import time
import datetime
import asyncio
import get_objects
import dbsqlalch

def start():
    list_of_objects = get_objects.get_objects_receivers()    
    loopy(list_of_objects)

def loopy(list_of_objects):
    start = time.time()

    ioloop = asyncio.get_event_loop()

    tasks = [ioloop.create_task(get(i)) for i in list_of_objects]
        
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
            
    print(tic(start))
        
    # writing results in db
    save_results(list_of_objects) 
        
async def get(i):
    #print(i)
    try:
        await i.get_parameters()
    except:
        pass
    
    i.time = datetime.datetime.now().strftime("%H:%M")

def tic(start):
    return 'at %1.1f seconds' % (time.time() - start)

def print_obj(l):
    for i in l:
        print(i.c_n)

def save_results(list_of_objects):
    for i in list_of_objects:
        dbsqlalch.save(i.ip, i.port, i.time, i.c_n, i.eb_no, i.l_m)
        #print(i.ip, i.port, i.time, i.c_n, i.eb_no, i.l_m)

if __name__ == "__main__":
    start()
