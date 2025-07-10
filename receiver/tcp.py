#!/usr/bin/env python3
import socket
import sys
import threading
import signal

class TCPServer:
    def __init__(self, host='0.0.0.0', port=9002):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.clients = []
        
    def handle_client(self, client_sock, addr):
        """Handle individual client connections"""
        print(f"New connection from {addr[0]}:{addr[1]}")
        
        try:
            while self.running:
                # Receive data from client
                data = client_sock.recv(4096)
                
                if not data:
                    break
                    
                # Print received message
                message = data.decode('utf-8', errors='replace')
                print(f"Received from {addr[0]}:{addr[1]}: {message.strip()}")
                
        except socket.error as e:
            print(f"Client {addr[0]}:{addr[1]} error: {e}")
        except ConnectionResetError:
            print(f"Client {addr[0]}:{addr[1]} disconnected unexpectedly")
        finally:
            # Clean up client connection
            if client_sock in self.clients:
                self.clients.remove(client_sock)
            client_sock.close()
            print(f"Connection closed with {addr[0]}:{addr[1]}")
    
    def start(self):
        """Start the TCP server"""
        try:
            # Create TCP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Allow reuse of address
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to address and port
            self.sock.bind((self.host, self.port))
            
            # Listen for incoming connections (backlog of 5)
            self.sock.listen(5)
            
            self.running = True
            print(f"TCP server listening on {self.host}:{self.port}")
            print("Press Ctrl+C to stop")
            
            # Accept incoming connections
            while self.running:
                try:
                    # Accept new connection
                    client_sock, addr = self.sock.accept()
                    self.clients.append(client_sock)
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, addr),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                        break
                except KeyboardInterrupt:
                    break
                    
        except OSError as e:
            print(f"Error starting server: {e}")
            sys.exit(1)
        finally:
            self.stop()
    
    def stop(self):
        """Stop the TCP server"""
        self.running = False
        
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Close server socket
        if self.sock:
            self.sock.close()
        print("\nServer stopped")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal")
    sys.exit(0)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse command line arguments
    port = 9002
    host = '0.0.0.0'
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    # Create and start server
    server = TCPServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop()

if __name__ == "__main__":
    print("start")
    main()