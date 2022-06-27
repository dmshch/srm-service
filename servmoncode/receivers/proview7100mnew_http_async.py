# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

'''
For schema:
1 TS RF IN <-> 1 TS IP OUT
2 TS RF IN <-> 2 TS IP OUT
3 TS RF IN <-> 3 TS IP OUT
4 TS RF IN <-> 4 TS IP OUT
'''

class ProView7100mnew(receiverbase.Receiver):

    async def get_parameters(self):

        HOST = self.ip
        user = self.login
        password = self.password

        request_payload = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'><get-all><filter type="subtree"><AravaPortV1 Id="1300000''' + self.port + '''"/></filter></get-all></hconf>'''

        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:
            # For RF value
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                #print("Status:", response.status, "\n")
                html = await response.text()
                #print(html)

            # For CC errors and service
            s1 = '''<?xml version="1.0"?><hconf source="SAG" xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='./hconf.xsd'>'''
            s2 = '''<get-all><filter type="subtree"><Platform Id="4000001"/></filter></get-all></hconf>'''
            request_payload = s1 + s2
            async with session.post("http://" + self.ip + "/BrowseConfig.pvr", data = request_payload) as response:
                #print("Status:", response.status, "\n")
                html_cc = await response.text()
                #print(html_cc)

        # For RF value
        out_list = html.split()
        # '<BER>0.00000000</BER>', '<DetEbN0>15.29</DetEbN0>', '<C0n>16.70</C0n>', '<LinkMargin>9.79</LinkMargin>'
        out_data = dict()
        for i in range(len(out_list)):
            if "C0n" in out_list[i]:
                out_data["C/N"] = out_list[i].replace("<C0n>", "").replace("</C0n>", "")
            if "DetEbN0" in out_list[i]:
                out_data["Eb/N0"] = out_list[i].replace("<DetEbN0>", "").replace("</DetEbN0>", "")
            if "LinkMargin" in out_list[i]:
                out_data["Link Margin"] = out_list[i].replace("<LinkMargin>", "").replace("</LinkMargin>", "")
            if "BER" in out_list[i]:
                out_data["BER"] = out_list[i].replace("<BER>", "").replace("</BER>", "")

        # For CC Errors
        out_list = html_cc.split("\n")
        flag = False
        out_data["CC Errors"] = "n/a"
        for i in range(len(out_list)):
            if """<OutputTs Id="5000000""" + self.port + """">""" in out_list[i]:
                flag = True
                continue
            if flag and "<TsCcErrors>" in out_list[i]:
                out_data["CC Errors"] = out_list[i].replace("<TsCcErrors>","").replace("</TsCcErrors>","")
                break

        # For services
        services = ""
        flag = False
        for i in range(len(out_list)):
            if '<OutputTs Id="5000000' + self.port + '">' in out_list[i]:
                flag = True
            if "</OutputPmts>" in out_list[i] and flag is True:
                break
            if "<ProgramNum>" in out_list[i] and flag is True:
                services += out_list[i].replace("<ProgramNum>","").replace("</ProgramNum>","").strip() + " "

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]
        self.cc = out_data["CC Errors"]
        self.service = services
        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
