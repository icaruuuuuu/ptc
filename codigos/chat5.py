from socket import *
from threading import Thread, Lock
import json

PORTA = int(input('Digite sua porta: '))
peers = []
peers_lock = Lock()  # Para proteger o acesso à lista de peers

def start_server(porta):
    servidor = socket(AF_INET, SOCK_STREAM)
    servidor.bind(('0.0.0.0', porta))
    servidor.listen(10)

    try:
        while True:
            conn, addr = servidor.accept()
            # with peers_lock:
            #     peers.append(addr)
            Thread(target=handle_peers, args=(conn, addr), daemon=True).start()
    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        servidor.close()

def handle_peers(conn, addr):
    print(f'Conexão estabelecida com {addr}')

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                msg = data.decode('utf-8')

                if msg == '/peersplease':
                    with peers_lock:
                        conexoes = [f'{ip}:{porta}' for ip, porta in peers]
                    conn.sendall(json.dumps(conexoes).encode('utf-8'))
                elif msg[0:3] == '/s ':
                    peer = msg[3:].split(':')
                    peer[1] = int(peer[1])
                    peer = tuple(peer)

                    with peers_lock:
                        peers.append(peer)
                else:
                    print(f'{addr}: {msg}')
            except Exception as e:
                print(f"Erro ao processar mensagem de {addr}: {e}")
    except Exception as e:
        print(f"Erro na conexão com {addr}: {e}")
    finally:
        conn.close()
        with peers_lock:
            if addr in peers:
                peers.remove(addr)

def send_msg(peer: tuple, msg: str):
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(peer)
        client.sendall(msg.encode('utf-8'))
    except Exception as e:
        print(f"Não foi possível enviar a mensagem para {peer}: {e}")
    finally:
        client.close()

def connect(peer: tuple):
    global peers
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(peer)
        client.sendall('/peersplease'.encode('utf-8'))
        client.sendall(f'/s {client.getsockname()[0]}:{PORTA}'.encode('utf-8'))

        data = client.recv(4096)
        n_peers = json.loads(data.decode('utf-8'))

        with peers_lock:
            for peer_str in n_peers:
                ip, porta = peer_str.split(':')
                peer_tuple = (ip, int(porta))
                if peer_tuple not in peers:
                    peers.append(peer_tuple)
    except Exception as e:
        print(f"Erro ao conectar com {peer}: {e}")
    finally:
        client.close()

def main():
    print('Iniciando...')
    Thread(target=start_server, args=(PORTA,), daemon=True).start()

    while True:
        entr = input()

        if entr.startswith('/c '):
            try:
                ip, porta = entr[3:].split(':')
                peer = (ip, int(porta))
                connect(peer)
            except Exception as e:
                print(f"Socket inválido: {e}")
        else:
            with peers_lock:
                for peer in peers:
                    send_msg(peer, entr)


main()