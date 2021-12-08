# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

class ProView7000(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><AravaPortV1 Id="1300000''' + self.port + '''"/></filter></get-all></hconf>'''

        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                #print("Status:", response.status, "\n")
                html = await response.text()
                #print(html)

            """
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
            """

        out_list = html.split()

        out_data = dict()
        for i in range(len(out_list)):
            if "<C0n>" in out_list[i]:
                out_data["C/N"] = out_list[i].replace("<C0n>", "").replace("</C0n>", "")
            if "<EbN0>" in out_list[i]:
                out_data["Eb/N0"] = out_list[i].replace("<EbN0>", "").replace("</EbN0>", "")
            if "LinkMargin" in out_list[i]:
                out_data["Link Margin"] = out_list[i].replace("<LinkMargin>", "").replace("</LinkMargin>", "")
            if "BER" in out_list[i]:
                out_data["BER"] = out_list[i].replace("<BER>", "").replace("</BER>", "")

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)

    
