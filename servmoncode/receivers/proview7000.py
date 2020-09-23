# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import getpass
import telnetlib
from . import receiverbase

class ProView7000(receiverbase.Receiver):

    def get_parameters(self):
        #for ProView 7000 

        HOST = self.ip
        user = self.login
        password = self.password

        tn = telnetlib.Telnet(HOST)

        tn.read_until(b"(none) login:")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password:")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"status/interface/input/port/rf/dvb/satellite_2/port_status 1\n")
        tn.write(b"exit\n")

        out_list = tn.read_all().decode('ascii').split("|")
        out_data = dict()

        for i in range(len(out_list)):
            if "fe_C_N_status" in out_list[i]:
                out_data["fe_C_N_status"] = out_list[i+1].strip()
            if "fe_Eb_N0_status" in out_list[i]:
                out_data["fe_Eb_N0_status"] = out_list[i+1].strip()
            if "fe_link_margin_status" in out_list[i]:
                out_data["fe_link_margin_status"] = out_list[i+1].strip()

        self.c_n = out_data["fe_C_N_status"]
        self.eb_no = out_data["fe_Eb_N0_status"]
        self.l_m = out_data["fe_link_margin_status"]
