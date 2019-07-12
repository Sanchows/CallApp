import asyncio

async def handle_echo(reader, writer):
    while True:
        data = await reader.read(256)
        if not data:
            break

        writer.write(data)
        await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())