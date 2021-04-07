# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

#for ProView 7000

#

import asyncio
import telnetlib3
from . import receiverbase

class ProView7000(receiverbase.Receiver):

    async def get_parameters(self):
        
        reader, writer = await telnetlib3.open_connection(host=self.ip, port=23, shell = None)
        # shell (Callable) – A asyncio.coroutine() that is called after negotiation completes, receiving arguments (reader, writer).
        # The reader is a TelnetReader instance,
        # the writer is a TelnetWriter instance.

        data = await reader.readuntil(separator=b':')

        message = self.login + "\n"
        writer.write(message)
        await writer.drain()

        data = await reader.readuntil(separator=b':')

        message = self.password + "\n"
        writer.write(message)
        await writer.drain()

        data = await reader.readuntil(separator=b'>')

        message = "status/interface/input/port/rf/dvb/satellite_2/port_status 1\n"
        writer.write(message)
        await writer.drain()

        data = await reader.readuntil(separator=b'>')
        
        out_list = data.decode('ascii').split("|")
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
        
        writer.close()
        #await writer.wait_closed()
