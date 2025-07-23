import asyncio
from asyncio import StreamReader, StreamWriter
from functools import partial
import socket
import ssl

from . import HOST, PORT

async def handle_client(
    reader: StreamReader,
    writer: StreamWriter
) -> None:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("/certs/server.crt", "/certs/server.key")

    print("tls Client connected", flush=True)
    await writer.start_tls(ctx)

    while True:
        data = await reader.readline()
        if data == b"":
            break
        message = data.decode('utf8').rstrip()
        print(f"Read data: {message}")
            
    print("Closing client")
    writer.close()
    await writer.wait_closed()
    print("Client closed")

async def run_server():
    print("Starting server", flush=True)
    server = await asyncio.start_server(handle_client, HOST, PORT)

    async with server:
        await server.serve_forever()

asyncio.run(run_server())