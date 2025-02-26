from socket import *
from threading import Thread
import json

PORTA = int(input('Digite sua porta: '))
peers = []

def start_server(porta:int):
    servidor = socket(AF_INET, SOCK_STREAM)
    servidor.bind(('0.0.0.0', porta))
    servidor.listen(10)

    global peers
    try:    
        while True:
            conn, addr = servidor.accept()
            peers.append(addr)
            Thread(target=handle_peers, args=(conn, addr), daemon=True).start()
    except:
        pass
    finally:
        for conn, addr in peers:
            conn.close()
        servidor.close()


def handle_peers(conn, addr):
    print(f'positivo {addr}')

    # global peers
    # conexoes = [f'{addr[0]}:{addr[1]}' for _, addr in peers]
    # conn.sendall(json.dumps(conexoes).encode('utf-8'))

    while True:
        data = conn.recv(4096)
        if not data:
            break
        try:
            msg = json.loads(data.decode('utf-8'))

            if msg == 'peersplease':
                global peers
                conexoes = [f'{addr[0]}:{addr[1]}' for _, addr in peers]
                conn.sendall(json.dumps(conexoes).encode('utf-8'))
            else:
                print(f'{addr}: {msg}')
        except:
            print(f"Erro ao tratar coneção com {addr}")
            conn.close()

def send_msg(peer:tuple, msg:str):
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(peer)
        client.sendall(msg.encode('utf-8'))
    except:
        print(f"não foi possível enviar a mensagem para {peer}")
    finally:
        client.close()

def connect(peer:tuple):
    global peers
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(peer)
    client.sendall('peersplease')

    data = client.recv(4096)
    n_peers = list(data.decode('utf-8'))
    for i in range(len(n_peers)):
        n_peers[i].split(':')
        n_peers[i] = (n_peers[i][0], int(n_peers[i][1]))

        if n_peers[i] not in peers: peers.append(n_peers[i])
    # print(f"não foi possível se conectar com {peer}")

    client.close()

def main():
    print('Iniciando...')
    Thread(target=start_server, args=PORTA, daemon=True).start()

    while(True):
        entr = input()
        
        if entr[0:3] == '/c ':
            try:
                client = entr[3:].split(':')
                client[1] = int(client[1])
                client = tuple(client)
            except: 
                print('Socket inválido.')
                continue

            connect(client)
        
        else:
            for peer in peers:
                send_msg(peer)

main()


# start_server(PORTA)