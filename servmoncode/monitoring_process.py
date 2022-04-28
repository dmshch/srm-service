# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import time
import datetime
import asyncio
from servmoncode import get_objects
from servmoncode import dbsqlalch
import traceback
from aiohttp.client_exceptions import ClientConnectorError

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
    
    print(datetime.datetime.now().strftime("%G %b %d %H:%M") + ". " +  "Polling time was: " + tic(start))

    # Save new stats and delete old stats >= 1 month
    dbsqlalch.DB().save(list_of_objects)
    
async def get(i):
    #print(i)
    try:
        await i.get_parameters()
    except BaseException as err:
        #print(traceback.format_exc())
        if type(err) is ClientConnectorError:
            #print("connection error")
            i.c_n, i.eb_no, i.l_m = "connection error", "connection error", "connection error"
        else:
            #print("parsing error")
            print(err)
            i.c_n, i.eb_no, i.l_m = "parsing error", "parsing error", "parsing error"
    
    i.time = datetime.datetime.now().strftime("%G %b %d %H:%M")

def tic(start):
    return 'at %1.1f seconds' % (time.time() - start)

