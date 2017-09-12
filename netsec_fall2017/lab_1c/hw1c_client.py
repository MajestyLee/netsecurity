#!/usr/bin/python3
#made by libinjie 09/07/2017, for creating Test_client
import asyncio
import sys
sys.path.append("..")
import lab_1_Packet.RequestConvert
import lab_1_Packet.ConvertAnswer
import lab_1_Packet.Result
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
class EchoClinetProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.status = 0
        self.loop = loop
        self.transport = None
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, lab_1_Packet.ConvertAnswer) and self.status == 0:
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
                # self.transport.write(self.answer)
                self.status += 1
            elif isinstance(pkt, lab_1_Packet.Result) and self.status == 1:
                # print(pkt)
                print('Data received: {!r}'.format(pkt.Judge))
                self.status += 1
            else:
                # print(pkt.Judge)
                print('Data received: {!r}'.format(pkt))  
    def connection_lost(self, exc):
        self.transport = None
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()
    def SendData(self, answer):
        if isinstance(answer, lab_1_Packet.ConvertAnswer) and self.status == 1:
            print('Data sent: {!r}'.format(answer.Value + " " + answer.numType))
        elif isinstance(answer, lab_1_Packet.RequestConvert) and self.status == 0:
            print('Data sent: {!r}'.format("request"))
        else:
            pass
            # print('sent a wrong packet')
        self.transport.write(answer.__serialize__())