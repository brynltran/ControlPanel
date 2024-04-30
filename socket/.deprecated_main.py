import socket

def start_server():

    server_ip = '192.168.1.2'
    server_port = 1013

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind((server_ip, server_port))
    try:
        server_socket.listen()

        client_socket, addr = server_socket.accept()

    finally:
        client_socket.close()

start_server()
