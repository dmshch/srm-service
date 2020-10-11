# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from pathlib import *
import sqlite3
from servmoncode import db

#edit settings from web gui

# load all settings as dict 
def get_settings():
    settings, receiver_authentication, user_authentication = dict(), dict(),dict()
    
    return settings, receiver_authentication, user_authentication

def get_global_settings():
    pass

def get_users_settings():
    pass

def get_receivers_settings():
    pass
