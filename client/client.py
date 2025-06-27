import socket
import os
import ssl

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

context = ssl.create_default_context()
context.load_verify_locations("/certs/cert.pem")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_hostname=HOST)
conn.connect((HOST, PORT))
conn.sendall(b"Hello, world")
data = conn.recv(1024)

print(f"Received {data!r}")

conn.shutdown(socket.SHUT_RDWR)
conn.close()