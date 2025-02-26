from threading import Thread, Lock
from socket import *
from json import *

# Funções de QOL
def get_hostname() -> str:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('1.1.1.1', 80))
        return s.getsockname()[0]
    
def tuple_to_socket(addr:tuple) -> str:
    return f'{addr[0]}:{addr[1]}'

def socket_to_tuple(s:str) -> tuple:
    aux = s.split(':')
    aux[1] = int(aux[1])
    addr = (aux[0], aux[1])
    return addr

def get_peers() -> str:
    global peers
    r = ''
    with peers_lock:
        for peer in peers:
            r += str(peer) + ' '
    return r

def get_conexoes() -> str:
    global conexoes
    r = ''

    with conexoes_lock:
        for c in conexoes:
            r += str(c.getsockname()) + ' '
    return r

def troca_peers(conn:socket) -> None:
    global peers

    data = conn.recv(4096)
    novos_peers = loads(data.decode('utf-8')).split()

    compat = dumps(get_peers())
    conn.sendall(compat.encode('utf-8'))

    with peers_lock:
        peers += novos_peers

    # for p in novos_peers:
    #     connect(p)

def manda_peers(conn:socket) -> None:
    global peers

    compat = dumps(get_peers())
    conn.sendall(compat.encode('utf-8'))
    
    data = conn.recv(4096)
    novos_peers = loads(data.decode('utf-8')).split()

    with peers_lock:
        peers += novos_peers

    # for p in novos_peers:
    #     connect(p)


# Funções do app
def start_server() -> None:
    global PORTA, peers
    servidor = socket(AF_INET, SOCK_STREAM)
    servidor.bind(('0.0.0.0', PORTA))
    print(f"Servidor escutando em 0.0.0.0:{PORTA}...")
    servidor.listen(5)

    try:
        while True:
            conn, addr = servidor.accept()
            print(f'Conexão com {addr}')
            troca_peers(conn)
            Thread(target=handle_peers, args=(conn, addr), daemon=True).start()
    except Exception as e:
        print(f'Erro ao manter servidor: {e}')
    finally:
        servidor.close()

def handle_peers(conn:socket, addr:tuple):
    global peers
    
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            msg = data.decode('utf-8')
            print(f'{addr}: {msg}')
    except Exception as e:
        print(f'Erro ao tratar conexão com {addr}: {e}')
    finally:
        with peers_lock:
            if addr in peers: peers.remove(addr)

def connect(addr:str) -> None:
    global HOST, PORTA, peers, conexoes
    # with peers_lock:
    #     if addr not in peers: peers.append(addr)
    addr = socket_to_tuple(addr)

    try:
        peer = socket(AF_INET, SOCK_STREAM)
        # peer.bind((HOST, PORTA+1))
        peer.connect(addr)
        manda_peers(peer)
    except Exception as e:
        print(e)
    finally:
        with conexoes_lock:
            conexoes += [peer]


def send_msg(conn:socket, msg:str) -> None:
    try:
        conn.sendall(msg.encode('utf-8'))
    except Exception as e:
        print(f'Erro ao enviar mensagem para {conn.getsockname()[0]}: {e}')


# Obtendo informações iniciais
HOST = get_hostname()
PORTA = int(input('Digite a porta: '))
peers = [tuple_to_socket((HOST, PORTA))]
conexoes = []
peers_lock = Lock()
conexoes_lock = Lock()

# Código principal
def main():
    global peers
    try:
        Thread(target=start_server, daemon=True).start() # Iniciando o servidor
        print('App iniciado.')
    except Exception as e:
        print(e)


    while True:
        entrada = input()
        if entrada.split()[0] == '/connect':
            connect(entrada.split()[1])
            continue

        if entrada == '/peers':
            print(get_peers())
            continue

        if entrada == '/conexoes':
            print(get_conexoes())
            continue

        with peers_lock:
            for peer in conexoes:
                    send_msg(peer, entrada)
        
main()