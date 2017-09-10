#!/usr/bin/python3
#made by libinjie 09/04/2017, for creating 3 packets and doing unit tests
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
#Homework 1(a) packet1
class RequestConvert(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.RequestConvert" #id
    DEFINITION_VERSION = "1.0" #version
#Homework 1(a) 2 and 3 are the same packettype, so it can identify the same one, they all include (ID,Value,type)
class ConvertAnswer(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.ConvertAnswer" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("ID", UINT32),
        ("Value", STRING),
        ("numType", STRING) #ROMAN OR INT
    ]
#Homework 1(a) packet4
class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.libinjie.Result" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("ID", UINT32),
        ("Judge", STRING) #SuccessFail
    ]
def basicUnitTest():
    packet1 = RequestConvert()
    packet1Bytes = packet1.__serialize__()
    packet1a = RequestConvert.Deserialize(packet1Bytes)
    assert packet1 == packet1a #judge if serialize and deserialize
    packet2 = ConvertAnswer()
    packet2.ID = 1
    packet2.Value = "XII"
    packet2.numType = "ROMAN"
    packet2Bytes = packet2.__serialize__()
    packet2a = ConvertAnswer.Deserialize(packet2Bytes)
    assert packet2 == packet2a #judge if serialize and deserialize normal result
    # packet2.ID = -1
    # assert packet2 == packet2a #ID <0, error
    # packet2.ID = 4294967297
    # assert packet2 == packet2a #ID >2^32-1, error
    # packet2.ID = "1"
    # assert packet2 == packet2a #ID is not the type of "uint",error
    packet3 = ConvertAnswer()
    packet3.ID = 1
    packet3.Value = "12"
    packet3.numType = "INT"
    packet3Bytes = packet3.__serialize__()
    packet3a = ConvertAnswer.Deserialize(packet3Bytes)
    assert packet3 == packet3a #judge if serialize and deserialize
    # assert packet2a == packet3a
    packet4 = Result()
    packet4.ID = 1
    packet4.Judge = "Success"
    packet4Bytes = packet4.__serialize__()
    packet4a = Result.Deserialize(packet4Bytes)
    assert packet4 == packet4a #judge if serialize and deserialize
    # test and output the deserializer result.
    # pktBytes = packet1Bytes + packet2Bytes + packet3Bytes + packet4Bytes
    # deserializer = PacketType.Deserializer()
    # while (len(pktBytes) > 0):
    #     chunk, pktBytes = pktBytes[:25], pktBytes[25:] #the first 25 ch
    #     deserializer.update(chunk)
    #     print(chunk.decode("utf-8")) #buffer to string, more clear
    #     print ("Another 25 bytes loaded into deserializer.Left={}".format(len(pktBytes)))
    #     for packet in deserializer.nextPackets():
    #         print ("got one!")
    #         if packet == packet1:
    #             print("it's 1!")
    #         elif packet == packet2:
    #             print("it's 2!")
    #         elif packet == packet3:
    #             print("it's 3!")
    #         elif packet == packet4:
    #             print("it's 4!")
    #         else:
    #             print("none")
if __name__=="__main__":
     basicUnitTest()
