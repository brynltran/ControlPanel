import socket

def start_server():
    host = '192.168.1.2'  # Localhost
    port = 1313        # Choose any port that is free on your system
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen()
    print("Server is listening on", host, port)
    
    while True:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print('Connected by', addr)
        
        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    break  # Break the loop if data is not received
                print("Received:", data.decode())
                
                # Optionally, send some data back
                client_socket.sendall(b'Echo => ' + data)
        except socket.error as e:
            print("Socket error:", e)
        finally:
            client_socket.close()

        print('Connection closed with', addr)

if __name__ == '__main__':
    start_server()

