# Copyright © 2021 Dmitrii Shcherbakov. All rights reserved.

from . import receiverbase
import aiohttp
import asyncio

class ProView2962(receiverbase.Receiver):

    async def get_parameters(self):
        #for ProView 2962 (WEB)

        HOST = self.ip
        user = self.login
        password = self.password

        request_payload = "p0=" + self.login + "&p1=" + self.password + "&p2=-1&p3=-1&p4=-1"

        auth = aiohttp.BasicAuth(login=self.login, password=self.password, encoding='utf-8')

        async with aiohttp.ClientSession(auth=auth) as session:
            #async with session.post("http://" + self.ip + "/_GetAttr.asp?action=Login", data = request_payload) as response:
                #print("Status:", response.status, "\n")
            
            async with session.get("http://" + self.ip + "/Status.asp") as response:

                #print("Status:", response.status)
                #print("Content-type:", response.headers['content-type'])

                html = await response.text()
                out_list = html.split("\n")

                #print(html)

        out_data = dict()

        for i in range(len(out_list)):
            if "C/N" in out_list[i] and "Eb/N0" in out_list[i] and "Link Margin" in out_list[i] and "BER" in out_list[i]:
                s_par = (out_list[i + 1])
            if "Continuity Counter" in out_list[i]:
                cc = (out_list[i + 3])
            if "Service Id" in out_list[i]:
                s_serv = (out_list[i + 1])
                break

        """ START  """
        s_par = s_par.replace("</td>","")
        s_par = s_par.split("<td nowrap>")
        cc = cc.replace("<td nowrap>","").replace("</td>","")
        #print(s_par)
        out_data["C/N"] = s_par[2]
        out_data["Eb/N0"] = s_par[3]
        out_data["Link Margin"] = s_par[4] 
        out_data["BER"] = s_par[5]
        out_data["CC Delta"] = cc
        """ END """
        
        """ START """
        s_serv = s_serv.replace("</td>","")
        s_serv = s_serv.split("<td nowrap>")
        #print(s_serv)
        out_data["Service"] = s_serv[3]
        """ END """
        
        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]
        self.service = out_data["Service"]
        self.cc_delta = out_data["CC Delta"]

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
