#!/usr/bin/env python3
import socket

from . import HOST, PORT

def start():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Allow reuse of address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to address and port
    sock.bind((HOST, PORT))
    
    running = True
    print(f"UDP server listening on {HOST}:{PORT}")
    
    # Listen for incoming messages
    while running:
        try:
            # Receive data (buffer size 4096 bytes)
            data, addr = sock.recvfrom(4096)
            
            # Print received message
            message = data.decode('utf-8', errors='replace')
            print(f"Received from {addr[0]}:{addr[1]}: {message}")
            
            # Echo the message back (optional - netcat behavior)
            sock.sendto(data, addr)
            
        except socket.error as e:
            if running:
                print(f"Socket error: {e}")
                break

start()