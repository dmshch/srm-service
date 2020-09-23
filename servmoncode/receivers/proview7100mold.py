# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

#status/interface/input/port/rf/dvb/satellite_2/port_status 1-4

import paramiko
import time
from . import receiverbase

class ProView7100mold(receiverbase.Receiver):
    #for ProView 7100 multi input, old soft
    def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        #/root/status/interface/input/port/rf/dvb/satellite_2/port_status 1

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=HOST, username=user, password=password, look_for_keys=False, allow_agent=False)

        with client.invoke_shell() as ssh:
            stdin, stdout, stderr = client.exec_command('status/interface/input/port/rf/dvb/satellite_2/port_status ' + self.port + '\n')
            data = stdout.read()

        client.close()

        out_list = str(data).split("|")

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
