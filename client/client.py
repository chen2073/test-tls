import socket
import ssl

def create_tls_client(host='localhost', port=8443):
    # Create SSL context for client
    context = ssl.create_default_context()
    
    # For self-signed certificates, disable hostname checking
    # Remove these lines when using proper certificates
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # Create socket and wrap with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tls_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to server
        tls_sock.connect((host, port))
        print(f"Connected to TLS server at {host}:{port}")
        
        # Send messages
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            tls_sock.send(message.encode('utf-8'))
            
            # Receive response
            response = tls_sock.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")
            
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        tls_sock.close()
        print("Connection closed")

if __name__ == "__main__":
    create_tls_client()