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
def basicUnitTest(): # test the loop instead of testloop
    print("")
    print("the test: client sent a packet")
    loop = asyncio.set_event_loop(TestLoopEx())
    client = hw1c_client.EchoClinetProtocol(loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    # assert server.data_received()
    Packet = lab_1_Packet.RequestConvert()
    client.SendData(Packet)
    assert client.status == 1
    assert server.status == 1
    Packet = lab_1_Packet.ConvertAnswer()
    Packet.ID = 1
    Packet.Value = "12"
    Packet.numType = "INT"
    client.SendData(Packet)
    assert client.status == 1
    assert server.status == 1
    Packet = lab_1_Packet.ConvertAnswer()
    Packet.ID = 1
    Packet.Value = "15"
    Packet.numType = "INT"
    client.SendData(Packet)
    assert client.status == 1
    assert server.status == 1
def basicUnitTest_2():
    loop = asyncio.set_event_loop(TestLoopEx())
    client = hw1c_client.EchoClinetProtocol(loop)
    server = hw1c_server.EchoServerClientProtocol()
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    server.connection_made(transportToClient)
    client.connection_made(transportToServer)
    print("")
    print("the test: client sent a wrong packet")
    Packet = ErrorPacket()
    Packet.Error = "error"
    client.SendData(Packet)
    assert client.status == 0
    assert server.status == 0
if __name__=="__main__":
    basicUnitTest()
    basicUnitTest_2()
    print("Basic Unit Test Successful.")
