#!/usr/bin/python3
#made by libinjie 09/04/2017, for creating 3 packets and doing unit tests
import unittest
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
#Homework 1(a) packet1
class TEST(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.RequestConvert" #id
    DEFINITION_VERSION = "1.0" #version
    FIELD = [
        ("ID", UINT32),
        ("TT", ListFieldType(STRING)),
        ("numType", STRING)
        ]
def basicUnitTest():
    packet1 = TEST()
    packet1.ID = 1
    packet1.TT = []
    packet1.TT.append("123")
    packet1.numType = "dasa"
    print(packet1.TT)
    packet1Bytes = packet1.__serialize__()
    packet1a = TEST.Deserialize(packet1Bytes)
    print(packet1)
    print(packet1a)
    assert packet1 == packet1a #judge if serialize and deserialize
if __name__=="__main__":
     basicUnitTest()