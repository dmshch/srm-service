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

        """ C/N (dB) """
        self.c_n = "not initialized"

        """ Eb/N0 (dB) """
        self.eb_no = "not initialized"

        """ Link Margin (dB) """
        self.l_m = "not initialized"
        
        """ Time of update """ 
        self.time = "not initialized"

        """ List of services (one or more) """
        self.service = "not initialized"

        """ Delta (for period of update) for CC errors"""
        self.cc = "not initialized"
