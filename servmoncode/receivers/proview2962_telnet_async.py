# Copyright © 2020 Dmitrii Shcherbakov. All rights reserved.

#for ProView 2962

import asyncio
from . import receiverbase

class ProView2962(receiverbase.Receiver):

    async def get_parameters(self):
        reader, writer = await asyncio.open_connection(self.ip, 23)

        data = await reader.readuntil(separator=b':')
        #print(f'Received: {data!r}')

        message = self.login + "\n"
        #print(f'{message!r}')
        writer.write(message.encode())
        await writer.drain()
        
        data = await reader.readuntil(separator=b':')
        #print(f'Received: {data!r}')

        message = self.password + "\n"
        #print(f'{message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        #print(f'Received: {data!r}')

        message = "status/receiver/quality\n"
        #print(f'{message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.readuntil(separator=b'root>')
        #print(f'Received: {data!r}')

        message = "exit\n"
        #print(f'{message!r}')
        writer.write(message.encode())
        await writer.drain()

        out_list = data.decode('ascii').split("|")
        out_data = dict()
        for i in range(len(out_list)):
            if "Signal Quality" in out_list[i]:
                out_data["Signal Quality"] = out_list[i+1].strip()
            if "C/N" in out_list[i]:
                out_data["C/N"] = out_list[i+1].strip()
            if "Eb/N0" in out_list[i]:
                out_data["Eb/N0"] = out_list[i+1].strip()
            if "Link Margin" in out_list[i]:
                out_data["Link Margin"] = out_list[i+1].strip()
            if "BER" in out_list[i]:
                out_data["BER"] = out_list[i+1].strip()

        self.c_n = out_data["C/N"]
        self.eb_no = out_data["Eb/N0"]
        self.l_m = out_data["Link Margin"]

        #print('Close the connection')
        writer.close()
        await writer.wait_closed()

        #print("ip:" +self.ip + " c_n:" + self.c_n + " eb_no:" + self.eb_no + " l_m:" +  self.l_m)
        
