#!/usr/bin/python3
#made by libinjie 09/07/2017, for creating Result
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
#Homework 1(a) packet4
class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.Result" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("ID", UINT32),
        ("Judge", STRING) #SuccessFail
    ]