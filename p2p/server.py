import asyncio
import sys
import json

peers = []
peers_data = []

async def processing(reader, writer):
    peername = writer.get_extra_info('peername')
    
    peer_data = {'peername': peername, 'writer': writer}
    
    print(f"Connected peer {peername}")
    
    # send information to peer about connected peer
    pd = json.dumps(peers)

    writer.write('peers'.encode() + pd.encode())
    await writer.drain()
    # -

    # send information to peers about new connection of peer to the server
    if len(peers) > 0:
        for dct in peers_data:
            wr = dct['writer']
            wr.write(f'NEW PEER: {peername}'.encode())
            await wr.drain()
    # -
    
    peers.append(peername) 
    peers_data.append(peer_data)

    while True:
        try:
            await asyncio.sleep(0.01)
            writer.write('.'.encode())
            await writer.drain()

        except ConnectionResetError:
            break
        except BrokenPipeError:
            break
    
    peers_data.remove(peer_data)
    peers.remove(peername)
    
    for dct in peers_data:
        wr = dct['writer']
        wr.write(f'***** disc:{peername}'.encode())
        await wr.drain()
    
    print(f"Peer {peername} disconnected from server.")
    


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