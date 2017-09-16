import sys, time, os, logging, asyncio
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.common import *
from playground.network.devices import *
sys.path.append("..")
import lab_1_Packet.RequestConvert
import lab_1_Packet.ConvertAnswer
import lab_1_Packet.Result
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, ListFieldType, BOOL
class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self._deserializer = PacketType.Deserializer()
        self.transport = None
        self.status = 0
    def connection_made(self, transport):
        print("server ok")
        self.transport = transport
    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, lab_1_Packet.RequestConvert) and self.status == 0:
                self.status += 1
                Packet = lab_1_Packet.ConvertAnswer()
                Packet.ID = 1
                Packet.Value = "XII"
                Packet.numType = "ROMAN"
                print('Server Send: {!r}'.format(Packet.Value + " " + Packet.numType))
                self.transport.write(Packet.__serialize__())
                print("Data received request")
            elif isinstance(pkt, lab_1_Packet.ConvertAnswer) and self.status == 1:
                self.status += 1
                print('Data received: {!r}'.format(pkt.Value + " " + pkt.numType))
                packet4 = lab_1_Packet.Result()
                packet4.ID = 1
                if str(self.romanToInt(self, "XII")) == pkt.Value:
                    packet4.Judge = "Success"
                    print('Server Send: {!r}'.format(packet4.Judge))
                    self.transport.write(packet4.__serialize__())
                else:
                    packet4.Judge = "Fail"
                    print('Server Send: {!r}'.format(packet4.Judge))
                    self.transport.write(packet4.__serialize__())
            else:
                print("error")
                self.transport.close()
                return
    def connection_lost(self, exc):
        self.transport.close()
        print('Echo Server Connection Lost because {!r}'.format(exc))
    @staticmethod
    def romanToInt(self, s): # judge if the result is right
        buff_dict = {}
        buff_dict['M'] = 1000
        buff_dict['D'] = 500
        buff_dict['C'] = 100
        buff_dict['L'] = 50
        buff_dict['X'] = 10
        buff_dict['V'] = 5
        buff_dict['I'] = 1 # define roman
        summary = 0
        for i in range(0,len(s)-1):
            if buff_dict[s[i]] < buff_dict[s[i+1]]:
                summary -= buff_dict[s[i]] # IV,IX
            else:
                summary += buff_dict[s[i]]
        return summary + buff_dict[s[len(s)-1]] # add the last
class EchoClinetProtocol(asyncio.Protocol):
    def __init__(self, callback = None):
        self.buffer = ""
        if callback:
            self.callback = callback
        else:
            self.callback = print
        self.transport = None
        self._deserializer = PacketType.Deserializer()
        self.status = 0
    def connection_made(self, transport):
        print("ok")
        self.transport = transport
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
            print("request")
            # print("1223")
            Packet = lab_1_Packet.RequestConvert()
            self.transport.write(Packet.__serialize__())
        else:
            Packet = lab_1_Packet.ConvertAnswer()
            Packet.ID = 1
            Packet.Value = answer
            Packet.numType = "INT"
            self.transport.write(Packet.__serialize__())

class EchoControl:
    def __init__(self):
        self.txProtocol = None
        
    def buildProtocol(self):
        return EchoClinetProtocol(self.callback)
        
    def connect(self, txProtocol):
        self.txProtocol = txProtocol
        print("Echo Connection to Server Established!")
        # self.txProtocol = txProtocol
        # print("Enter Message: ", end="")
        
    def callback(self, message):
        print("Server Response: {}".format(message))
        
    def stdinAlert(self):
        data = sys.stdin.readline()
        if data and data[-1] == "\n":
            # print("input ok")
            data = data[:-1] # strip off \n
        self.txProtocol.SendData(data)
class clientpassthrough(StackingProtocol):
    def __init__(self):
        super().__init__
    def data_received(self, data):
        print("psclient received")
        self.higherProtocol().data_received(data)
    def connection_made(self, transport):
        print("psclient con made")
        self.transport = transport
        self.higherProtocol().connection_made(StackingTransport(self.transport))
        # self.higherProtocol.transport = transport
    def connection_lost(self, exc):
        print("psclient con lost")
        self.transport.close()
        self.higherProtocol().transport.close()
class serverpassthrough(StackingProtocol):
    def __init__(self):
        super().__init__
    def data_received(self, data):
        print("server received")
        self.higherProtocol().data_received(data)
    def connection_made(self, transport):
        print("server con made")
        self.transport = transport
        self.higherProtocol().connection_made(StackingTransport(self.transport))
        # self.higherProtocol.transport = transport
    def connection_lost(self, exc):
        print("server con lost")
        self.transport.close()
        self.higherProtocol().transport.close()
    # def SendData(self, data):
    #     self.higherProtocol().SendData(data)
USAGE = """usage: echotest <mode>
  mode is either 'server' or a server's address (client mode)"""

if __name__=="__main__":
    echoArgs = {}
    args= sys.argv[1:]
    i = 0
    for arg in args:
        if arg.startswith("-"):
            k,v = arg.split("=")
            echoArgs[k]=v
        else:
            echoArgs[i] = arg
            i+=1
    
    if not 0 in echoArgs:
        sys.exit(USAGE)

    mode = echoArgs[0]
    loop = asyncio.get_event_loop()
    f = StackingProtocolFactory(lambda: clientpassthrough(),lambda: Serverpassthrough())
    ptConnector = playground.Connector(protocolStack=f)
    playground.setConnector("passthrough", ptConnector)
    if mode.lower() == "server":
        coro = playground.getConnector('passthrough').create_playground_server(lambda: EchoServerProtocol(), 726)
        server = loop.run_until_complete(coro)
        print("Echo Server Started at {}".format(server.sockets[0].gethostname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        loop.close()
        
        
    else:
        remoteAddress = mode
        control = EchoControl()
        coro = playground.getConnector().create_playground_connection(control.buildProtocol, remoteAddress, 726)
        transport, protocol = loop.run_until_complete(coro)
        print("Echo Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))
        loop.add_reader(sys.stdin, control.stdinAlert)
        control.connect(protocol)
        loop.run_forever()
        loop.close()