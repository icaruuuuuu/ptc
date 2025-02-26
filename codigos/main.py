from threading import Thread, Lock
from socket import *
from json import *

# Funções de QOL
def get_hostname() -> str:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('1.1.1.1', 80))
        return s.getsockname()[0]
    
def tuple_to_socket(addr: tuple) -> str:
    return f'{addr[0]}:{addr[1]}'

def socket_to_tuple(s: str) -> tuple:
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
            try:
                # Verifica se a conexão ainda está ativa
                c.getpeername()  # Testa se o socket ainda está conectado
                r += tuple_to_socket(c.getpeername()) + ' '
            except:
                # Remove conexões inativas
                conexoes.remove(c)
    return r

def connect_to_new_peers(new_peers: list) -> None:
    global HOST, PORTA, peers, conexoes

    for peer_addr in new_peers:
        # Evita conectar a si mesmo
        if peer_addr == tuple_to_socket((HOST, PORTA)):
            continue

        # Evita conectar a peers já conhecidos
        with peers_lock:
            if peer_addr in peers:
                continue

        # Tenta conectar ao novo peer
        try:
            print(f"Tentando conectar a {peer_addr}...")
            connect(peer_addr)
        except Exception as e:
            print(f"Erro ao conectar a {peer_addr}: {e}")

def troca_peers(conn: socket) -> None:
    global peers

    data = conn.recv(4096)
    novos_peers = loads(data.decode('utf-8')).split()

    compat = dumps(get_peers())
    conn.sendall(compat.encode('utf-8'))

    with peers_lock:
        peers += novos_peers

    # Conecta aos novos peers
    connect_to_new_peers(novos_peers)

def manda_peers(conn: socket) -> None:
    global peers

    compat = dumps(get_peers())
    conn.sendall(compat.encode('utf-8'))
    
    data = conn.recv(4096)
    novos_peers = loads(data.decode('utf-8')).split()

    with peers_lock:
        peers += novos_peers

    # Conecta aos novos peers
    connect_to_new_peers(novos_peers)

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
            with conexoes_lock:
                conexoes.append(conn)
            Thread(target=handle_peers, args=(conn, addr), daemon=True).start()
    except Exception as e:
        print(f'Erro ao manter servidor: {e}')
    finally:
        servidor.close()

def handle_peers(conn: socket, addr: tuple):
    global peers
    
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            msg = data.decode('utf-8')
            print(f'{addr}: {msg}')

            # Envia a mensagem apenas para os peers diretamente conectados
            with conexoes_lock:
                for c in conexoes:
                    if c.getpeername() != addr:  # Evita enviar de volta para o remetente
                        try:
                            c.sendall(msg.encode('utf-8'))
                        except Exception as e:
                            print(f'Erro ao enviar mensagem para {c.getpeername()}: {e}')
    except Exception as e:
        print(f'Erro ao tratar conexão com {addr}: {e}')
    finally:
        with conexoes_lock:
            conexoes.remove(conn)
        with peers_lock:
            if addr in peers: peers.remove(addr)

def connect(addr: str) -> None:
    global HOST, PORTA, peers, conexoes
    addr = socket_to_tuple(addr)

    try:
        peer = socket(AF_INET, SOCK_STREAM)
        peer.connect(addr)
        manda_peers(peer)
        with conexoes_lock:
            conexoes.append(peer)
        Thread(target=handle_peers, args=(peer, addr), daemon=True).start()
    except Exception as e:
        print(e)

def send_msg(conn: socket, msg: str) -> None:
    try:
        conn.sendall(msg.encode('utf-8'))
    except Exception as e:
        print(f'Erro ao enviar mensagem para {conn.getpeername()}: {e}')

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

        with conexoes_lock:
            for conn in conexoes:
                send_msg(conn, entrada)
        
        with peers_lock: peers = [peers[0]] + list(set(peers[1:]))
        
main()
