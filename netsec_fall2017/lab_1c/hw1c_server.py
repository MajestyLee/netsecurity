#!/usr/bin/python3
#made by libinjie 09/07/2017, for testing TCPechoserver
#TCP echo server protocol¶
import asyncio
import sys
sys.path.append("..")
import lab_1_Packet.RequestConvert
import lab_1_Packet.ConvertAnswer
import lab_1_Packet.Result
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
class EchoServerClientProtocol(asyncio.Protocol):
    def __init__(self):
        # self.Packet = Packet
        # self.loop = loop
        self.transport = None
    def connection_made(self, transport):
        # peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(peername))
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
    def data_received(self, data):
        packet1 = lab_1_Packet.RequestConvert()
        packet3 = lab_1_Packet.ConvertAnswer()
        packet3.ID = 1
        packet3.Value = "12"
        packet3.numType = "INT"
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, lab_1_Packet.ConvertAnswer):
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
            elif isinstance(pkt, lab_1_Packet.Result):
                print('Data received: {!r}'.format(pkt.Judge))
            elif isinstance(pkt, lab_1_Packet.RequestConvert):
                print('Data received: {!r}'.format("request"))
            else:
                print("unknown received packet")
            # print('Data received: {!r}'.format(ppkktt))
        if isinstance(pkt, lab_1_Packet.RequestConvert):
            Packet = lab_1_Packet.ConvertAnswer()
            Packet.ID = 1
            Packet.Value = "XII"
            Packet.numType = "ROMAN"
            print('Server Send: {!r}'.format(Packet.Value + " " + Packet.numType))
            self.transport.write(Packet.__serialize__())
        elif isinstance(pkt, lab_1_Packet.ConvertAnswer):
            packet4 = lab_1_Packet.Result()
            packet4.ID = 1
            if str(self.romanToInt(self, "XII")) == pkt.Value:
                packet4.Judge = "Success"
                print('Server Send: {!r}'.format(packet4.Judge))
                self.transport.write(packet4.__serialize__())
            else:
                packet4.Judge = "Fail"
                print('Server Send: {!r}'.format(packet4.Judge))
                self.transport.write(packet4.__serialize__())
        else:
            print ("error and do not return to the client")
    def connection_lost(self, exc):
        self.transport = None
        print('Echo Server Connection Lost because {!r}'.format(exc))
    @staticmethod
    def romanToInt(self, s): # judge if the result is right
        buff_dict = {}
        buff_dict['M'] = 1000
        buff_dict['D'] = 500
        buff_dict['C'] = 100
        buff_dict['L'] = 50
        buff_dict['X'] = 10
        buff_dict['V'] = 5
        buff_dict['I'] = 1 # define roman
        summary = 0
        for i in range(0,len(s)-1):
            if buff_dict[s[i]] < buff_dict[s[i+1]]:
                summary -= buff_dict[s[i]] # IV,IX
            else:
                summary += buff_dict[s[i]]
        return summary + buff_dict[s[len(s)-1]] # add the last
        # print('Close the client socket')
        # self.transport.close()
# loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
# coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
# server = loop.run_until_complete(coro)

# # Serve requests until Ctrl+C is pressed
# print('Serving on {}'.format(server.sockets[0].getsockname()))
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass

# Close the server
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()