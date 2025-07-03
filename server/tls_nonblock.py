import asyncio
import ssl
import socket
import select

from . import HOST, PORT

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="/certs/cert.pem", keyfile="/certs/key.pem")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
client_socket = None

# waiting on client socket
while not client_socket:
    ready, _, _ = select.select([server_socket], [], [], 1.0)
    
    if server_socket in ready:
        try:
            client_sock, addr = server_socket.accept()
            print(f"Client connected from {addr}")
            
            # Set non-blocking and wrap with SSL
            client_sock.setblocking(False)
            client_socket = context.wrap_socket(
                client_sock, 
                server_side=True, 
                do_handshake_on_connect=False
            )
        except socket.error as e:
            print(f"Error accepting connection: {e}")

# handle_client
handshake_complete = None
while client_socket:
    read_ready = []
    write_ready = []
    
    # Determine what to monitor
    if not handshake_complete:
        read_ready = [client_socket]
        write_ready = [client_socket]
    else:
        read_ready = [client_socket]
    
    # Wait for socket activity
    readable, writable, error = select.select(
        read_ready, write_ready, [client_socket], 1.0
    )
    
    # Handle errors first
    if client_socket in error:
        print("Client connection error")
        break
    
    # Handle SSL handshake
    if not handshake_complete:
        try:
            client_socket.do_handshake()
            handshake_complete = True
            print("SSL handshake completed")
            continue
        except Exception as e:
            print(f"handshake fail {e}")
            break
    
    # Handle data
    if client_socket in readable:
        try:
            data = client_socket.recv(1024)
            if data:
                message = data.decode('utf-8').strip()
                print(f"Received: {message}")
                
                # Echo response
                response = f"Echo: {message}\n"
                client_socket.send(response.encode('utf-8'))
            else:
                print("Client disconnected")
        except Exception as e:
            print(f"error receiving data {e}")



# async def handler(reader, writer):
#     await writer.start_tls()
#     data = await reader.read(100)
#     message = data
#     addr = writer.get_extra_info('peername')

#     print(f"Received {message!r} from {addr!r}")

#     print(f"Send: {message!r}")
#     writer.write(data)
#     await writer.drain()

#     print("Close the connection")
#     writer.close()
#     await writer.wait_closed()

# async def main():
#     server = await asyncio.start_server(handler, HOST, PORT)

#     addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
#     print(f'Serving on {addrs}')

#     async with server:
#         await server.serve_forever()

# asyncio.run(main())