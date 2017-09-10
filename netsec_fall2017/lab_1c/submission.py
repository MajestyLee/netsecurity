#!/usr/bin/python3
#made by libinjie 09/08/2017, for unit testing client and server
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import hw1c_client
import hw1c_server
import asyncio
import sys
sys.path.append("..")
import lab_1_Packet.RequestConvert
import lab_1_Packet.ConvertAnswer
import lab_1_Packet.Result
class ErrorPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.ErrorPacket" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("Error", STRING)
    ] #test by using the wrong packet
def basicUnitTest_1(): # test the loop instead of testloop
    print("")
    print("the true test: client sent a packet")
    Packet = lab_1_Packet.ConvertAnswer()
    Packet.ID = 1
    Packet.Value = "15"
    Packet.numType = "INT"
    loop = asyncio.get_event_loop()
    client = hw1c_client.EchoClinetProtocol(Packet,loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
def basicUnitTest_2(): #use testloop
    print("")
    print("the first test: client sent a wrong packet")
    loop = asyncio.set_event_loop(TestLoopEx())
    Packet = ErrorPacket()
    Packet.Error = "error"
    client = hw1c_client.EchoClinetProtocol(Packet,loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    print("")
    print("")
    print("the second test: client sent a request packet,server return a roman number,hw1a step1 and 2")
    Packet = lab_1_Packet.RequestConvert()
    client = hw1c_client.EchoClinetProtocol(Packet,loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    print("")
    print("")
    print("the third test: client sent the right answer packet,server return the result,hw1a step3 and 4")
    Packet = lab_1_Packet.ConvertAnswer()
    Packet.ID = 1
    Packet.Value = "12"
    Packet.numType = "INT"
    client = hw1c_client.EchoClinetProtocol(Packet,loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    print("")
    print("")
    print("the fourth test: client sent the wrong answer packet,server return the result,hw1a step3 and 4")
    Packet = lab_1_Packet.ConvertAnswer()
    Packet.ID = 1
    Packet.Value = "15"
    Packet.numType = "INT"
    client = hw1c_client.EchoClinetProtocol(Packet,loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
if __name__=="__main__":
    basicUnitTest_1()
    basicUnitTest_2()
    print("Basic Unit Test Successful.")
