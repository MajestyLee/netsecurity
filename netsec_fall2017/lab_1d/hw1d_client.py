#!/usr/bin/python3
#made by libinjie 09/07/2017, for creating Test_client
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
class EchoClinetProtocol(asyncio.Protocol):
    def __init__(self, loop, callback = None):
        self.buffer = ""
        if callback:
            self.callback = callback
        else:
            self.callback = print
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self.status = 0
        self.loop = loop
    def connection_made(self, transport):
        print("ok")
        self.transport = transport
        # self._deserializer = PacketType.Deserializer()
    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, lab_1_Packet.ConvertAnswer) and self.status == 0:
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
                self.callback(pkt.Value)
                # self.transport.write(self.answer)
                self.status += 1
            elif isinstance(pkt, lab_1_Packet.Result) and self.status == 1:
                # print(pkt)
                print('Data received: {!r}'.format(pkt.Judge))
                # self.callback()
                self.status += 1
            else:
                # print(pkt.Judge)
                print('Data received: {!r}'.format(pkt))  
    def connection_lost(self, exc):
        self.transport.close()
        print('The server closed the connection')
        print('Stop the event loop')
        # self.loop.stop()
    def SendData(self, answer):
        if answer == 'request':
            print("1223")
            Packet = lab_1_Packet.RequestConvert()
            self.transport.write(Packet.__serialize__())
        else:
            Packet = lab_1_Packet.ConvertAnswer()
            Packet.ID = 1
            Packet.Value = answer
            Packet.numType = "INT"
            self.transport.write(Packet.__serialize__())
        # if isinstance(answer, lab_1_Packet.ConvertAnswer) and self.status == 1:
        #     print('Data sent: {!r}'.format(answer.Value + " " + answer.numType))
        # elif isinstance(answer, lab_1_Packet.RequestConvert) and self.status == 0:
        #     print('Data sent: {!r}'.format("request"))
        # else:
        #     print('sent a wrong packet')
        # self.transport.write(answer.__serialize__())
class EchoControl:
    def __init__(self):
        self.txProtocol = None
        
    def buildProtocol(self, loop):
        return EchoClinetProtocol(loop, self.callback)
        
    def connect(self, txProtocol):
        self.txProtocol = txProtocol
        print("Echo Connection to Server Established!")
        self.txProtocol = txProtocol
        print("Enter Message: ", end="")
        
    def callback(self, message):
        print("Server Response: {}".format(message))
        
    def stdinAlert(self):
        data = sys.stdin.readline()
        if data and data[-1] == "\n":
            print("input ok")
            data = data[:-1] # strip off \n
        self.txProtocol.SendData(data)

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    control = EchoControl()
    # control.connect(EchoClinetProtocol())
    coro = playground.getConnector().create_playground_connection(control.buildProtocol(loop), '20174.1.1.1', 101)
    # print(coro)
    transport, protocol = loop.run_until_complete(coro)
    # transport, protocol = loop.run_until_complete(coro)
    print("made ok")
    loop.add_reader(sys.stdin, control.stdinAlert)
    control.connect(protocol)
    loop.run_forever()
    loop.close()


# loop = asyncio.get_event_loop()
# print(loop)
# message = "none"
# print(EchoClinetProtocol(message, loop))
# Packet = lab_1_Packet.RequestConvert()
# client = EchoClinetProtocol()
# client.SendData(Packet)
# coro = playground.getConnector().create_playground_connection (client,
#                               '20174.1.1.1', 8888)
# loop.run_until_complete(coro)
# loop.run_forever()
# loop.close()