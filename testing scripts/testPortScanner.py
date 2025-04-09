import socket
import sys
import threading
import time

def http_server(connection):
    """Simulate a basic HTTP server"""
    try:
        # Receive client request
        data = connection.recv(1024)
        
        # Send HTTP response
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Test HTTP Server</h1></body></html>"
        connection.sendall(response.encode())
    except:
        pass
    finally:
        connection.close()

def ftp_server(connection):
    """Simulate a basic FTP server"""
    try:
        # Send FTP welcome banner
        welcome = "220 Test FTP Server Ready\r\n"
        connection.sendall(welcome.encode())
        
        # Handle a simple command
        data = connection.recv(1024)
        if data:
            response = "530 Please login with USER and PASS.\r\n"
            connection.sendall(response.encode())
    except:
        pass
    finally:
        connection.close()

def ssh_server(connection):
    """Simulate a basic SSH server"""
    try:
        # Send SSH banner
        ssh_banner = "SSH-2.0-OpenSSH_Test_Server\r\n"
        connection.sendall(ssh_banner.encode())
        
        # Just receive data and do nothing with it
        connection.recv(1024)
    except:
        pass
    finally:
        connection.close()

def smtp_server(connection):
    """Simulate a basic SMTP server"""
    try:
        # Send SMTP greeting
        greeting = "220 localhost.localdomain SMTP Test Server\r\n"
        connection.sendall(greeting.encode())
        
        # Handle a command
        data = connection.recv(1024)
        if data:
            response = "250 localhost.localdomain\r\n"
            connection.sendall(response.encode())
    except:
        pass
    finally:
        connection.close()

def generic_server(connection):
    """Generic service that just keeps connection open"""
    try:
        # Send a generic welcome message
        welcome = "Welcome to test service\r\n"
        connection.sendall(welcome.encode())
        
        # Wait for some data
        connection.recv(1024)
    except:
        pass
    finally:
        connection.close()

def create_socket(port, service_type):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to localhost on the specified port
    server_address = ('localhost', port)
    print(f"Starting {service_type} server on port {port}")
    
    try:
        server_socket.bind(server_address)
        # Listen for incoming connections
        server_socket.listen(5)
        
        print(f"Socket successfully created on port {port}")
        print("Press Ctrl+C to exit")
        
        # Keep the socket open until manually interrupted
        while True:
            # Wait for a connection
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            # Handle connection based on service type
            if service_type == "http":
                threading.Thread(target=http_server, args=(connection,)).start()
            elif service_type == "ftp":
                threading.Thread(target=ftp_server, args=(connection,)).start()
            elif service_type == "ssh":
                threading.Thread(target=ssh_server, args=(connection,)).start()
            elif service_type == "smtp":
                threading.Thread(target=smtp_server, args=(connection,)).start()
            else:
                threading.Thread(target=generic_server, args=(connection,)).start()
            
    except KeyboardInterrupt:
        print("\nShutting down server")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            service = "generic"
            
            if len(sys.argv) > 2:
                service = sys.argv[2].lower()
            
            valid_services = ["http", "ftp", "ssh", "smtp", "generic"]
            if service not in valid_services:
                print(f"Invalid service type. Please use one of: {', '.join(valid_services)}")
                sys.exit(1)
                
            create_socket(port, service)
        except ValueError:
            print("Please provide a valid port number")
    else:
        print("Usage: python service_simulator.py [port_number] [service_type]")
        print("Example: python service_simulator.py 8080 http")
        print("Available service types: http, ftp, ssh, smtp, generic")