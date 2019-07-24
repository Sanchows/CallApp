import asyncio
import sys
import pickle

class Main():
    async def tcp_echo_client(self):

        reader, writer = await asyncio.open_connection(
            'localhost', 8888)

        while True:
            writer.write('HELLO!'.encode())
            await writer.drain()
            peers = await reader.read(256)
            
            print(pickle.loads(peers))

        print('Close the connection')
        writer.close()
try:
    asyncio.run(Main().tcp_echo_client())
except KeyboardInterrupt:
    sys.exit(0)