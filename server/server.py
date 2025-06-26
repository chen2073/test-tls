import socket
import os

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()
with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)

server_socket.close()