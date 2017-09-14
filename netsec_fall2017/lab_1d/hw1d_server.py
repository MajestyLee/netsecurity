#!/usr/bin/python3
#made by libinjie 09/07/2017, for testing TCPechoserver
#TCP echo server protocol¶
import sys, time, os, logging, asyncio
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.common import PlaygroundAddress
sys.path.append("..")
import lab_1_Packet.RequestConvert
import lab_1_Packet.ConvertAnswer
import lab_1_Packet.Result
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self._deserializer = PacketType.Deserializer()
        self.transport = None
        self.status = 0
    def connection_made(self, transport):
        print("server ok")
        self.transport = transport
        # print("connection ok")
    def data_received(self, data):
        # print("ok")
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            # print(pkt)
            if isinstance(pkt, lab_1_Packet.RequestConvert) and self.status == 0:
                self.status += 1
                Packet = lab_1_Packet.ConvertAnswer()
                Packet.ID = 1
                Packet.Value = "XII"
                Packet.numType = "ROMAN"
                print('Server Send: {!r}'.format(Packet.Value + " " + Packet.numType))
                self.transport.write(Packet.__serialize__())
                print("Data received request")
            elif isinstance(pkt, lab_1_Packet.ConvertAnswer) and self.status == 1:
                self.status += 1
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
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
                print("error")
                # self.transport.close()
    def connection_lost(self, exc):
        self.transport.close()
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

loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)
# Each client connection will create a new protocol instance
# playground.getConnector().create_playground_server(EchoServerClientProtocol, '8888')
coro = playground.getConnector().create_playground_server(lambda: EchoServerProtocol(), 101)
# print(coro)
server = loop.run_until_complete(coro)
print("Echo Server Started at {}".format(server.sockets[0].gethostname()))
# Serve requests until Ctrl+C is pressed
# print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
# server.close()
# loop.run_until_complete(server.wait_closed())
loop.close()