# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

import aiohttp
import asyncio
from . import receiverbase

class ProView7100mold(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:

            # New for RF status
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            request_payload = { "req":"CFG_ATTR_FE_GET_PORT_STATUS", "fe_port_number":self.port }
            async with session.post("http://" + self.ip + "/request2.esp", data = request_payload, headers = headers) as response:
                #print("Status:", response.status, "\n")
                html_test = await response.text()

            # New for Programs Numbers
            # Also there is program name like:
            # <cm_prog_name_hex>
            # <value>x01xbcxc3xb6xc1xbaxbexb5x20xbaxb8xbdxbe</value>
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            request_payload = { "req":"CFG_ATTR_GET_CNT_MGR_OUT_PROG_PARAMS", "cm_out_num":self.port }
            async with session.post("http://" + self.ip + "/request2.esp", data = request_payload, headers = headers) as response:
                #print("Status:", response.status, "\n")
                html_programs = await response.text()
                #print(html_programs)
        
        # RF status
        out_list_test = html_test.split()
        for i in range(len(out_list_test)):
            if "<fe_C_N_status>" in out_list_test[i]:
                c_n = out_list_test[i + 1].replace("<value>","").replace("</value>","").strip()
            if "<fe_Eb_N0_status>" in out_list_test[i]:
                eb_no  = out_list_test[i + 1].replace("<value>","").replace("</value>","").strip()
            if "<fe_link_margin_status>" in out_list_test[i]:
                l_m = out_list_test[i + 1].replace("<value>","").replace("</value>","").strip()

        # Programs Numbers
        service = ""
        out_list_srv = html_programs.split()
        for i in range(len(out_list_srv)):
            if "<cm_inp_prog>" in out_list_srv[i]:
                service += out_list_srv[i + 1].replace("<value>","").replace("</value>","") + " "

        self.c_n = c_n
        self.eb_no = eb_no
        self.l_m = l_m
        self.service = service

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
