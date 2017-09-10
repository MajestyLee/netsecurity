#!/usr/bin/python3
#made by libinjie 09/07/2017, for creating RequestConvert
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
#Homework 1(a) packet1
class RequestConvert(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.RequestConvert" #id
    DEFINITION_VERSION = "1.0" #version