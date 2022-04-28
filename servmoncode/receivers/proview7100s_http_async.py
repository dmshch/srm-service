# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

class ProView7100s(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password
        """
        request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><AravaPortV1 Id="1300000''' + self.port + '''"/></filter></get-all></hconf>'''
        """
        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:
            
            out_data = dict()

            # New - Get C/N, Eb/N0, Link Margin
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            request_payload = { "req":"CFG_ATTR_FE_GET_PORT_STATUS", "fe_port_number":"1" }
            async with session.post("http://" + self.ip + "/request2.esp", data = request_payload, headers = headers) as response:
                #print("Status:", response.status, "\n")
                html2 = await response.text()
                #print(self.ip)
                #print("test\n", html2)

            # For service and CC
            s1 = """<hconf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:noNamespaceSchemaLocation="./hconf.xsd" source="EMS"><get-all><filter type="subtree">"""
            s2 = """<PVR-7K Id="1000001"><Platform Id="4000001" /></PVR-7K></filter></get-all></hconf>"""
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            request_payload = s1 + s2
            async with session.post("http://" + self.ip + "/BrowseConfig", data = request_payload, headers = headers) as response:
                html_srv_cc = await response.text()
                #print(html_srv_cc)

        # C/N, Eb/N0, Link Margin
        out_list = html2.split()
        for i in range(len(out_list)):
            if "<fe_C_N_status>" in out_list[i]:
                out_data["C/N"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")
            if "<fe_Eb_N0_status>" in out_list[i]:
                out_data["Eb/N0"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")
            if "<fe_link_margin_status>" in out_list[i]:
                out_data["Link Margin"] = out_list[i + 1].replace("<value>", "").replace("</value>", "")
            
        # CC and service
        out_list_srv_cc = html_srv_cc.split()
        for i in range(len(out_list_srv_cc)):
            if "<CcErrors>" in out_list_srv_cc[i]:
                cc = out_list_srv_cc[i].replace("<CcErrors>","").replace("</CcErrors>","")
            if "<SelectedInputProgram>" in out_list_srv_cc[i]:
                program = out_list_srv_cc[i].replace("<SelectedInputProgram>","").replace("</SelectedInputProgram>","")
        out_data["CC Errors"] = cc
        out_data["Service"] = program        

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]        
        self.cc_delta = out_data["CC Errors"]
        self.service = out_data["Service"]
            
        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
