import socket
import ssl
import select
import errno

from . import HOST, PORT

class SimpleSSLServer:
    def __init__(self, host: str = 'localhost', port: int = 8443, 
                 certfile: str = 'server.crt', keyfile: str = 'server.key'):
        self.host = host
        self.port = port
        
        # Create SSL context
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile, keyfile)
        
        self.server_socket = None
        self.client_socket = None
        self.handshake_complete = False
        
    def start(self):
        """Start the server and handle one client"""
        # Create and setup server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        
        print(f"SSL Server listening on {self.host}:{self.port}")
        print("Waiting for client connection...")
        
        try:
            self.wait_for_client()
            if self.client_socket:
                self.handle_client()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.cleanup()
    
    def wait_for_client(self):
        """Wait for a single client connection"""
        while not self.client_socket:
            ready, _, _ = select.select([self.server_socket], [], [], 1.0)
            
            if self.server_socket in ready:
                try:
                    client_sock, addr = self.server_socket.accept()
                    print(f"Client connected from {addr}")
                    
                    # Set non-blocking and wrap with SSL
                    client_sock.setblocking(False)
                    self.client_socket = self.ssl_context.wrap_socket(
                        client_sock, 
                        server_side=True, 
                        do_handshake_on_connect=False
                    )
                    
                except socket.error as e:
                    if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                        print(f"Error accepting connection: {e}")
    
    def handle_client(self):
        """Handle the connected client"""
        print("Handling client connection...")
        
        while self.client_socket:
            read_ready = []
            write_ready = []
            
            # Determine what to monitor
            if not self.handshake_complete:
                read_ready = [self.client_socket]
                write_ready = [self.client_socket]
            else:
                read_ready = [self.client_socket]
            
            # Wait for socket activity
            readable, writable, error = select.select(
                read_ready, write_ready, [self.client_socket], 1.0
            )
            
            # Handle errors first
            if self.client_socket in error:
                print("Client connection error")
                break
            
            # Handle SSL handshake
            if not self.handshake_complete:
                if self.perform_handshake():
                    continue
                else:
                    break
            
            # Handle data
            if self.client_socket in readable:
                if not self.handle_read():
                    break
    
    def perform_handshake(self):
        """Perform SSL handshake"""
        try:
            self.client_socket.do_handshake()
            self.handshake_complete = True
            print("SSL handshake completed")
            return True
            
        except ssl.SSLWantReadError:
            # Need more data, continue
            return True
        except ssl.SSLWantWriteError:
            # Need to write, continue
            return True
        except ssl.SSLError as e:
            print(f"SSL handshake failed: {e}")
            return False
        except Exception as e:
            print(f"Handshake error: {e}")
            return False
    
    def handle_read(self):
        """Handle reading data from client"""
        try:
            data = self.client_socket.recv(4096)
            if data:
                message = data.decode('utf-8').strip()
                print(f"Received: {message}")
                
                # Echo response
                response = f"Echo: {message}\n"
                self.client_socket.send(response.encode('utf-8'))
                return True
            else:
                print("Client disconnected")
                return False
                
        except ssl.SSLWantReadError:
            # No data available yet
            return True
        except ssl.SSLWantWriteError:
            # SSL needs to write, but we're just reading
            return True
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            return False
        except socket.error as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                return True
            print(f"Socket error: {e}")
            return False
        except Exception as e:
            print(f"Read error: {e}")
            return False
    
    def cleanup(self):
        """Clean up connections"""
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        if self.server_socket:
            self.server_socket.close()
        
        print("Server cleanup complete")

# Example usage
if __name__ == "__main__":
    # Generate self-signed certificates for testing:
    # openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
    
    server = SimpleSSLServer(
        host=HOST,
        port=PORT,
        certfile="/certs/cert.pem",
        keyfile="/certs/key.pem"
    )
    
    server.start()