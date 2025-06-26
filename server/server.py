import socket
import ssl
import threading

def handle_client(conn, addr):
    """Handle individual client connections"""
    print(f"Connection from {addr}")
    
    try:
        while True:
            # Receive data from client
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Received from {addr}: {message}")
            
            # Echo the message back
            response = f"Server received: {message}"
            conn.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed")

def create_tls_server(host='localhost', port=8443):
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Load certificate and private key
    # You'll need to generate these files (see instructions below)
    context.load_cert_chain(certfile="/certs/server.crt", keyfile="/certs/server.key")
    
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Wrap socket with SSL
    tls_sock = context.wrap_socket(sock, server_side=True)
    
    try:
        # Bind and listen
        tls_sock.bind((host, port))
        tls_sock.listen(5)
        print(f"TLS Server listening on {host}:{port}")
        
        while True:
            # Accept connections
            conn, addr = tls_sock.accept()
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_client, 
                args=(conn, addr)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        tls_sock.close()

if __name__ == "__main__":
    print("test")
    create_tls_server()
