import socket
import os
import ssl

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="/certs/cert.pem", keyfile="/certs/key.pem")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()
conn_stream = context.wrap_socket(conn, server_side=True)
try:
    print(f"Connected by {addr}")
    while True:
        data = conn_stream.recv(1024)
        if not data:
            break
        conn_stream.sendall(data)
except Exception as e:
    print(f"err with tcp ssl: {e}")
finally:
    conn_stream.shutdown(socket.SHUT_RDWR)
    conn_stream.close()
