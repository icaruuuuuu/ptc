from socket import *

def cliente(host='127.0.0.1', porta=12346):
    c_socket = socket(AF_INET, SOCK_STREAM)
    c_socket.connect((host, porta))

    data = c_socket.recv(4096)
    print("Lista de conexões:", data.decode('utf-8'))
    c_socket.close()

cliente()