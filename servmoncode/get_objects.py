# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.
# Making and getting objects

from servmoncode import dbsqlalch

# sync
#from servmoncode.receivers import proview2962_telnet
#from servmoncode.receivers import proview7000_telnet
#from servmoncode.receivers import proview7100s_ssh
#from servmoncode.receivers import proview7100mold_ssh

# async
from servmoncode.receivers.proview2962_telnet_async import ProView2962
from servmoncode.receivers.proview7000_telnet_async import ProView7000
from servmoncode.receivers.proview7100s_ssh_async import ProView7100s
from servmoncode.receivers.proview7100mold_ssh_async import ProView7100mold
from servmoncode.receivers.proview8130_http_async import ProView8130
from servmoncode.receivers.proview7100mnew_http_async import ProView7100mnew

def get_objects_receivers():

    list_of_receivers = dbsqlalch.load_all_receivers()

    list_of_objects = []
    for i in list_of_receivers:
        ip, model, satellite, login, password, port, state, time, c_n, eb_no, l_m = i
        list_of_objects.append(return_object(ip, model, satellite, login, password, port, state))
            
    return list_of_objects

def return_object(ip, model, satellite, login, password, port, state):

    # getting default login and password, if they not set in receivers table
    if login == "" and password == "" or login == None and password == None:
        login, password = dbsqlalch.get_login_and_password(model)
        
    select_class = {
        "proview2962": ProView2962(ip, model, satellite, login, password, port, state),
        "proview7000": ProView7000(ip, model, satellite, login, password, port, state),
        "proview7100s": ProView7100s(ip, model, satellite, login, password, port, state),
        "proview7100mold": ProView7100mold(ip, model, satellite, login, password, port, state),
        "proview8130": ProView8130(ip, model, satellite, login, password, port, state),
        "proview7100mnew": ProView7100mnew(ip, model, satellite, login, password, port, state)
    }

    return select_class[model]


