import asyncio
import json


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost, loop):
        self.loop = loop
        self.on_con_lost = on_con_lost

    def data_received(self, data):
        if not data:
            pass

        msg = data.decode()
        
        if msg == '.':
            return
        
        print('Data received: {}'.format(msg))


    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(on_con_lost, loop),
        '127.0.0.1', 8889)

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())