#!/usr/bin/python3
#made by libinjie 09/26/2017, for creating Tcp packet
from playground.network.packet.fieldtypes.attributes import Optional
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import *
class Tcppacket(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.Tcppacket" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("Type", UINT8),
        ("SequenceNumber", UINT32({Optional: True})),
        ("Checksum", UINT16),
        ("Acknowledgement", UINT32({Optional: True})),
        ("Data", BUFFER({Optional: True}))
    ]