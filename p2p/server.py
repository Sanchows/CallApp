import asyncio
import pickle
import sys

peers = []

async def handle_echo(reader, writer):
    peername = writer.get_extra_info('peername')
    
    peers.append(peername) 
    #print(peers)
    while True:
        try:
            data = await reader.read(256)

            writer.write(pickle.dumps(peers))
            await writer.drain()
        except ConnectionResetError:
            break


    print(f"Peer {peername} disconnected from server.")
    writer.close()
    peers.remove(peername)

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    sys.exit(0)