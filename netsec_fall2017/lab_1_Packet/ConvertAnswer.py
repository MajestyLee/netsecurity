#!/usr/bin/python3
#made by libinjie 09/07/2017, for creating ConvertAnswer
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
#Homework 1(a) 2 and 3 are the same packettype, so it can identify the same one, they all include (ID,Value,type)
class ConvertAnswer(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.ConvertAnswer" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("ID", UINT32),
        ("Value", STRING),
        ("numType", STRING) #ROMAN OR INT
    ]