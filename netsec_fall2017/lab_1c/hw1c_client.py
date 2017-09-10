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
    def __init__(self, Packet, loop):
        self.Packet = Packet
        self.loop = loop
        self.transport = None
    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.Packet.__serialize__())
        if isinstance(self.Packet, lab_1_Packet.ConvertAnswer):
            print('Data sent: {!r}'.format(self.Packet.Value + " " + self.Packet.numType))
        elif isinstance(self.Packet, lab_1_Packet.Result):
            print('Data sent: {!r}'.format(self.Packet))
        elif isinstance(self.Packet, lab_1_Packet.RequestConvert):
            print('Data sent: {!r}'.format("request"))
        else:
            print('sent a wrong packet')
        # print('Data sent: {!r}'.format(self.Packet))
    def data_received(self, data):
        # pass
        self._deserializer = PacketType.Deserializer()
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, lab_1_Packet.ConvertAnswer):
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
            elif isinstance(pkt, lab_1_Packet.Result):
                print('Data received: {!r}'.format(pkt.Judge))
            else:
                print('Data received: {!r}'.format(pkt))
            # print(data.decode("utf-8"))
    def connection_lost(self, exc):
        self.transport = None
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()
# loop = asyncio.get_event_loop()
# print(loop)
# Packet = RequestConvert.RequestConvert()
# print(Packet)
# packet1Bytes = packet1.__serialize__()
# print(EchoClinetProtocol(message, loop))
# Packet = ConvertAnswer.ConvertAnswer()
# Packet.ID = 1
# Packet.Value = "12"
# Packet.numType = "INT"
# coro = loop.create_connection(lambda: EchoClinetProtocol(Packet, loop),
#                               '127.0.0.1', 8888)
# loop.run_until_complete(coro)
# loop.run_forever()
# loop.close()