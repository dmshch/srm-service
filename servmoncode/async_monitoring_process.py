# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import time
import datetime
import asyncio
import get_objects

def start():
    list_of_objects = get_objects.get_objects_receivers("active_only")
    print_obj(list_of_objects)
    loopy(list_of_objects)

def loopy(list_of_objects):
    flag = True
    while flag:
        start = time.time()

        ioloop = asyncio.get_event_loop()
        #ioloop = asyncio.get_running_loop()
        #ioloop = asyncio.new_event_loop()
        
        #asyncio.set_event_loop(ioloop)

        tasks = [ioloop.create_task(get(i)) for i in list_of_objects]
        
        print("task: ")
        print(tasks)
        
        wait_tasks = asyncio.wait(tasks)
        ioloop.run_until_complete(wait_tasks)
        ioloop.close()
            
        print(tic(start))

        #time.sleep(600)
        print_obj(list_of_objects)
        flag = False
        
async def get(i):
    print(i)
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

if __name__ == "__main__":
    start()
