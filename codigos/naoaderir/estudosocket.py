from socket import *
from threading import Thread
import json

arq = open('p')
PORTA = int(arq.readline())
arq.close()
peers = []

def start_server(porta):
    servidor = socket(AF_INET, SOCK_STREAM)
    servidor.bind(('0.0.0.0', porta))
    servidor.listen(10)

    global peers
    try:    
        while True:
            conn, addr = servidor.accept()
            peers.append((conn, addr))
            Thread(target=handle_peers, args=(conn, addr), daemon=True).start()
    except:
        pass
    finally:
        for conn, addr in peers:
            conn.close()
        servidor.close()


def handle_peers(conn, addr):
    print(f'positivo {addr}')

    global peers
    conexoes = [f'{addr[0]}:{addr[1]}' for _, addr in peers]
    conn.sendall(json.dumps(conexoes).encode('utf-8'))

    while True:
        data = conn.recv(4096)
        if not data:
            break
        try:
            print(f'{addr}: {data.decode('utf-8')}')
        except:
            print(f"Erro ao tratar coneção com {addr}")
            conn.close()


start_server(PORTA)
