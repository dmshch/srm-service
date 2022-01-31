# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

class ProView7000(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request_payload = { "req":"CFG_ATTR_GET_FE_PORT_DVB_SAT_STATUS", "cnt":"1", "p0":"1" }

        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:

            async with session.post("http://" + self.ip + "/request.esp", data = request_payload, headers = headers) as response:
                #print("Status:", response.status, "\n")
                html = await response.text()
                #print(self.ip)
                #print(html)
                flag = "B1"
            
            if "Unknown request" in html:

                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                request_payload = { "req":"CFG_ATTR_FE_GET_PORT_STATUS", "fe_port_number":"1" }

                async with session.post("http://" + self.ip + "/request2.esp", data = request_payload, headers = headers) as response:
                    #print("Status:", response.status, "\n")
                    html = await response.text()
                    #print(self.ip)
                    #print(html)
                    flag = "B2"

        out_list = html.split()
        out_data = dict()

        if flag == "B1":
            for i in range(len(out_list)):
                if "<data8>" in out_list[i]:
                    out_data["C/N"] = out_list[i + 2].replace("<value>", "").replace("</value>", "")
                if "<data9>" in out_list[i]:
                    out_data["Eb/N0"] = out_list[i + 2].replace("<value>", "").replace("</value>", "")
                if "<data10>" in out_list[i]:
                    out_data["Link Margin"] = out_list[i + 2].replace("<value>", "").replace("</value>", "")

        if flag == "B2":
            for i in range(len(out_list)):
                if "<fe_C_N_status>" in out_list[i]:
                    out_data["C/N"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")
                if "<fe_Eb_N0_status>" in out_list[i]:
                    out_data["Eb/N0"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")
                if "<fe_link_margin_status>" in out_list[i]:
                    out_data["Link Margin"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)

    
