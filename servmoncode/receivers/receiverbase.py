# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

# Base class

class Receiver:
    def __init__(self, ip, model, satellite, login, password, port, state):
        self.ip = ip
        self.model = model
        self.satellite = satellite
        self.login = login
        self.password = password
        self.port = port
        self.state = state

        self.time_of_update = ""
        
        """ Color of state object - red, green, yellow or white - for use in HTML page """
        self.color = "white"

        """ C/N (dB) """
        self.c_n = "not initialized"

        """ Eb/N0 (dB) """
        self.eb_no = "not initialized"

        """ Link Margin (dB) """
        self.l_m = "not initialized"
        
        """ Time of update """ 
        self.time = "not initialized"
