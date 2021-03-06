# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import asyncio
import asyncssh

from . import receiverbase

class ProView7100s(receiverbase.Receiver):
    #for ProView 7100 single input
    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        #/root/status/interface/input/port/rf/dvb/satellite_2/port_status 1

        command = 'status/interface/input/port/rf/dvb/satellite_2/port_status 1\n'

        async with asyncssh.connect(HOST, username=user, password=password, known_hosts = None) as conn:
            result = await conn.run(command, check=True)
            #print(result.stdout, end='')
            
        
            out_list = str(result).split("|")

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

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
