import asyncio
import sys
import json

peers = []

async def processing(reader, writer):
    peername = writer.get_extra_info('peername')

    peers.append(peername) 
    print(f"Connected peer {peername}")
    #print(peers)
    
    while True:
        try:
            pass
            #await asyncio.sleep(0.1)
            pd = json.dumps(peers, default=lambda o: o.__dict__)
            print(pd)
            writer.write(pd.encode())
            await writer.drain()

        except ConnectionResetError:
            break
        except BrokenPipeError:
            break

    
    print(f"Peer {peername} disconnected from server.")
    
    writer.write(f'disc:{peername}'.encode())
    peers.remove(peername)


async def main():
    server = await asyncio.start_server(
        processing, '127.0.0.1', 8889)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()
        
try:
    asyncio.run(main())
except KeyboardInterrupt:
    sys.exit(0)