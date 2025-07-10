import socket
# import threading

from . import HOST, PORT

# def start():
#     # Create TCP socket
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     # Allow reuse of address
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
#     sock.setblocking(False)

#     # Bind to address and port
#     sock.bind((HOST, PORT))
    
#     sock.listen(1)
    
#     running = True
#     print(f"TCP server listening on {HOST}:{PORT}", flush=True)

#     def receive():
#         while running:
#             try:
#                 conn, addr = sock.accept()
#                 data = conn.recv(4096)
#                 if not data:
#                     break
                    
#                 # Print received message
#                 message = data.decode('utf-8', errors='replace')
#                 print(f"Received from {addr[0]}:{addr[1]}: {message.strip()}")

#             except socket.error as e:
#                 if running:
#                     print(f"Socket error: {e}")
#                     break
    
#     threading.Thread(target=receive).start()

print("hihihihihihi", flush=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(4096)
            if not data:
                break