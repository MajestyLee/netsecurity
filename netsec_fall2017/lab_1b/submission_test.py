from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
class Mypacket(PacketType):
    DEFINITION_IDENTIFIER = "lab2b.binjieli.Mypacket" #id
    DEFINITION_VERSION = "1.0" #version
    FIELDS = [
        ("counter1", UINT32),
        ("counter2", UINT32),
        ("name", STRING),
        ("data", BUFFER)
    ]
packet1 = Mypacket() #if any field is null，serilize will fail
packet1.counter1 = 100
packet1.counter2 = 200
packet1.name = "libinjie"
packet1.data = b"this is packet1" #this is not string but a sequence of bytes。
packet2 = Mypacket() #if any field is null，serilize will fail
packet2.counter1 = 100
packet2.counter2 = 200
packet2.name = "libinjie"
packet2.data = b"this is packet2" #this is not string but a sequence of bytes。
packet3 = Mypacket() #if any field is null，serilize will fail
packet3.counter1 = 100
packet3.counter2 = 200
packet3.name = "libinjie"
packet3.data = b"this is packet3" #this is not string but a sequence of bytes。
packetBytes = packet1.__serialize__() #serialize,using to transport
pktBytes = packet1.__serialize__() + packet2.__serialize__() + packet3.__serialize__()
# packet2 = PacketType.Deserialize(packetBytes)
# # Deserializer solve enough to deserialize, if I need to deserialize more than 1 packet
# if packet1 == packet2:
#     print ("they are the same!")
# deserializer = PacketType.Deserializer()
# deserializer.update(data)
# for packet in deserializer.nextPackets():
#     #now I have a packet!
deserializer = PacketType.Deserializer()
print ("starting with {} bytes of data".format(len(pktBytes)))
while len(pktBytes) > 0:
    #let's take of a 20 byte chunk
    chunk, pktBytes = pktBytes[:20], pktBytes[20:]
    deserializer.update(chunk)
    print ("Another 20 bytes loaded into deserializer.Left={}".format(len(pktBytes)))
    for packet in deserializer.nextPackets():
        print ("got one!")
        if packet == packet1:
            print("it's 1!")
        elif packet == packet2:
            print("it's 2!")
        elif packet == packet3:
            print("it's 3!")
        else:
            print("none")