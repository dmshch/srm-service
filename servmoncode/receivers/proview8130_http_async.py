# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

class ProView8130(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password
        
        request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><AravaPortV1 Id="1300000''' + self.port + '''"/></filter></get-all></hconf>'''
        
        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:

            # Get C/N, Eb/N0, Link Margin
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                html = await response.text()
                #print(html)
                
            # Get IP-services
            request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><MainBoardV100 Id="5000001"/></filter></get-all></hconf>'''
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                html_ip_serv = await response.text()
                #print(html_ip_serv)

            # Get SDI-services
            request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><Platform Id="4000001"/></filter></get-all></hconf>'''
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                html_sdi_serv = await response.text()
                #print(html_sdi_serv)

        out_data = dict()
        
        # C/N, Eb/N0, Link Margin
        out_list = html.split()
        for i in range(len(out_list)):
            if "C0n" in out_list[i]:
                out_data["C/N"] = out_list[i].replace("<C0n>", "").replace("</C0n>", "")
            if "DetEbN0" in out_list[i]:
                out_data["Eb/N0"] = out_list[i].replace("<DetEbN0>", "").replace("</DetEbN0>", "")
            if "LinkMargin" in out_list[i]:
                out_data["Link Margin"] = out_list[i].replace("<LinkMargin>", "").replace("</LinkMargin>", "")
            if "BER" in out_list[i]:
                out_data["BER"] = out_list[i].replace("<BER>", "").replace("</BER>", "")
        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]

        # IP-services
        out_list = html_ip_serv.split("\n")
        str_of_service = "IP out: "
        for i in range(len(out_list)):
            if "<SelectedServiceName>" in out_list[i]:
                str_of_service += out_list[i].replace("<SelectedServiceName>", "").replace("</SelectedServiceName>", "").strip()
                str_of_service += "; "
        self.service = str_of_service
        out_data["Service"] = str_of_service

        # SDI-services
        out_list = html_sdi_serv.split("\n")
        str_of_service = "SDI out: "
        for i in range(len(out_list)):
            if "<SelectedInputProgram>" in out_list[i]:
                number_of_service = out_list[i].replace("<SelectedInputProgram>", "").replace("</SelectedInputProgram>", "").strip()
                flag = False
                for i in range(len(out_list)):
                    if ("<ProgramNumber>" + str(number_of_service) + "</ProgramNumber>") in out_list[i]:
                        flag = True
                    if flag == True and "<SelectedServiceName>" in out_list[i]:
                        str_of_service += out_list[i].replace("<SelectedServiceName>", "").replace("</SelectedServiceName>", "").strip()
                        break
        self.service += str_of_service
        out_data["Service"] += str_of_service
                    
        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m + " service:" + self.service)
