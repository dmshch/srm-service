# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import telnetlib

from . import receiverbase

class ProView2962(receiverbase.Receiver):
    
    def get_parameters(self):
        #for ProView 2962 

        HOST = self.ip
        user = self.login
        password = self.password

        tn = telnetlib.Telnet(HOST)

        tn.read_until(b"username:")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"password:")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"status/receiver/quality\n")
        tn.write(b"exit\n")

        out_list = tn.read_all().decode('ascii').split("|")
        out_data = dict()
        for i in range(len(out_list)):
            if "Signal Quality" in out_list[i]:
                out_data["Signal Quality"] = out_list[i+1].strip()
            if "C/N" in out_list[i]:
                out_data["C/N"] = out_list[i+1].strip()
            if "Eb/N0" in out_list[i]:
                out_data["Eb/N0"] = out_list[i+1].strip()
            if "Link Margin" in out_list[i]:
                out_data["Link Margin"] = out_list[i+1].strip()
            if "BER" in out_list[i]:
                out_data["BER"] = out_list[i+1].strip()

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]

