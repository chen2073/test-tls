import socket
import os

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")