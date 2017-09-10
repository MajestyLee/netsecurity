#!/usr/bin/python3
#made by libinjie 09/07/2017, for testing asyncio
#TCP echo client protocol¶
import asyncio
class TestProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.loop = loop
    def connection_made(self, transport):
        self.transport = transport
        # transport.write(self.message.encode())
        # print('Data sent: {!r}'.format(self.message))
    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()
loop = asyncio.get_event_loop()
# print(loop)
message = "none"
# print(EchoClinetProtocol(message, loop))
coro = loop.create_connection(lambda: EchoClinetProtocol(message, loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()