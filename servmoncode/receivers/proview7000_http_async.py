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
                    
            # For service and CC
            s1 = """<hconf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:noNamespaceSchemaLocation="./hconf.xsd" source="EMS"><get-all><filter type="subtree">"""
            s2 = """<PVR-7K Id="1000001"><Platform Id="4000001" /></PVR-7K></filter></get-all></hconf>"""
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            request_payload = s1 + s2
            async with session.post("http://" + self.ip + "/BrowseConfig", data = request_payload, headers = headers) as response:
                html_srv_cc = await response.text()
                #print(html_srv_cc)
 
        out_list = html.split()
        out_list_srv_cc = html_srv_cc.split()
        out_data = dict()
        
        for i in range(len(out_list_srv_cc)):
            if "<CcErrors>" in out_list_srv_cc[i]:
                cc = out_list_srv_cc[i].replace("<CcErrors>","").replace("</CcErrors>","")
            if "<SelectedInputProgram>" in out_list_srv_cc[i]:
                program = out_list_srv_cc[i].replace("<SelectedInputProgram>","").replace("</SelectedInputProgram>","")
        out_data["CC Errors"] = cc
        out_data["Service"] = program

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
        self.cc = out_data["CC Errors"]
        self.service = out_data["Service"]

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)

    
