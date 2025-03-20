from socket import *
from threading import Lock
from peersdb import peersdb
from utils import *

class ClientException(Exception):
    def init(self, msg):
        super.__init__(msg)

class Connections:
    def __init__(self):
        self.connections:set[socket] = set({})
        self.__lock = Lock()
    
    def __str__(self):
        return str(self.connections)
    
    def add(self, peer):
        with self.__lock:
            self.connections.add(peer)
    
    def remove(self, peer):
        with self.__lock:
            if peer in self.connections: self.connections.remove(peer)

class Client:
    def __init__(self):
        self.__connections = Connections()
        self.__concount = 0
    
    def connect(self, addr : tuple, hostname : str):
        global peersdb
        try:
            if addr[0] in ['127.0.0.1', '127.0.1.1']: raise ClientException('conexão com localhost não permitida')
            conn = socket(AF_INET, SOCK_STREAM)
            conn.connect(addr)
            print(f'Conexão estabelecida')
            self.update_connections(conn)
            self.send_peers(conn, peers_to_str(hostname, peersdb.peers))
            print(self.__connections)
            peersdb.add(tuple_to_socket(addr))
        except ClientException as e:
            print(f'Erro ao conectar-se com o peer: {e}')
        except Exception as e:
            print(f'Erro ao conectar-se com o peer: {e}')
            if conn in self.__connections.connections:
                self.__connections.remove(conn)
    
    def multi_connect(self, addrs:list[str], port):
        for addr in addrs:
            print(addr)
            if addr not in peersdb.peers:
                self.connect(socket_to_tuple(addr), obter_hostname(port))
    
    def send_msg(self, msg):
        # print(self.__connections)
        for c in self.__connections.connections:
            # print(f'Enviando mensagem para {c.getpeername()}')
            try: c.sendall(msg.encode('utf-8'))
            except Exception as e: 
                print(f'Erro ao enviar mensagem: {e}')
                self.__connections.remove(c)
                c.close()
    
    def send_peers(self, conn:socket, peers:str):
        conn.sendall(peers.encode('utf-8'))
    
    def update_connections(self, conn:socket):
        self.__connections.add(conn)
        self.__concount += 1
        # print(self.__connections)
    
    @property
    def connections(self):
        # print(self.__connections)
        return self.__connections.connections, self.__concount

cliente = Client()