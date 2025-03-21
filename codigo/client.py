from socket import *
from threading import Lock
from peersdb import peersdb
from utils import *

class ClientException(Exception):
    """
    Exceção personalizada para erros relacionados ao cliente.

    Esta exceção é levantada quando ocorre um erro específico relacionado às operações do cliente.
    """
    ...

class Connections:
    """
    Classe responsável por gerenciar as conexões de sockets.

    Esta classe mantém um conjunto de conexões de sockets e fornece métodos para adicionar e remover conexões.
    A classe também utiliza um Lock para garantir a segurança das operações em ambientes multithread.

    Attributes
    ----------
    connections : set[socket]
        Conjunto de sockets conectados.
    __lock : Lock
        Lock utilizado para garantir a segurança das operações em ambientes multithread.
    """

    def __init__(self):
        """Inicializa o conjunto de conexões e o Lock."""
        self.connections: set[socket] = set({})
        self.__lock = Lock()
    
    def __str__(self):
        """Retorna uma representação em string do conjunto de conexões."""
        return str(self.connections)
    
    def add(self, peer):
        """
        Adiciona um peer ao conjunto de conexões.

        Parameters
        ----------
        peer : socket
            O socket do peer a ser adicionado.
        """
        with self.__lock:
            self.connections.add(peer)
    
    def remove(self, peer):
        """
        Remove um peer do conjunto de conexões.

        Parameters
        ----------
        peer : socket
            O socket do peer a ser removido.
        """
        with self.__lock:
            if peer in self.connections: self.connections.remove(peer)

class Client:
    """
    Classe responsável por gerenciar o cliente no aplicativo de bate-papo P2P.

    Esta classe lida com a conexão com outros peers, envio de mensagens e atualização da lista de conexões.

    Attributes
    ----------
    __connections : Connections
        Instância da classe Connections para gerenciar as conexões.
    __concount : int
        Contador de conexões estabelecidas.
    """

    def __init__(self):
        """Inicializa o cliente com um conjunto de conexões e um contador de conexões."""
        self.__connections = Connections()
        self.__concount = 0
    
    def connect(self, addr: tuple, hostname: str):
        """
        Estabelece uma conexão com um peer.

        Parameters
        ----------
        addr : tuple
            Tupla contendo o endereço IP e a porta do peer.
        hostname : str
            Nome do host do peer.

        Raises
        ------
        ClientException
            Se a tentativa de conexão for com localhost.
        Exception
            Se ocorrer um erro durante a tentativa de conexão.
        """
        global peersdb
        try:
            if addr[0] in ['127.0.0.1', '127.0.1.1']: raise ClientException('conexão com localhost não permitida')
            conn = socket(AF_INET, SOCK_STREAM)
            conn.connect(addr)
            print(f'<SISTEMA>: Conexão estabelecida com {tuple_to_socket(addr)}')
            self.update_connections(conn)
            self.send_peers(conn, peers_to_str(hostname, peersdb.peers))
            peersdb.add(tuple_to_socket(addr))
        except ClientException as e:
            print(f'<SISTEMA>: Erro ao conectar-se com o peer {tuple_to_socket(addr)}: {e}')
        except Exception as e:
            print(f'<SISTEMA>: Erro ao conectar-se com o peer {tuple_to_socket(addr)}: {e}')
            if conn in self.__connections.connections:
                self.__connections.remove(conn)
    
    def send_msg(self, msg):
        """
        Envia uma mensagem para todos os peers conectados.

        Parameters
        ----------
        msg : str
            A mensagem a ser enviada.
        """
        for c in self.__connections.connections:
            try: c.sendall(msg.encode('utf-8'))
            except Exception as e: 
                print(f'<SISTEMA>: Erro ao enviar mensagem: {e}')
                self.__connections.remove(c)
                c.close()
    
    def send_peers(self, conn: socket, peers: str):
        """
        Envia a lista de peers para um peer específico.

        Parameters
        ----------
        conn : socket
            O socket do peer que receberá a lista de peers.
        peers : str
            A lista de peers em formato de string.
        """
        conn.sendall(peers.encode('utf-8'))
    
    def update_connections(self, conn: socket):
        """
        Atualiza a lista de conexões com um novo peer.

        Parameters
        ----------
        conn : socket
            O socket do peer a ser adicionado.
        """
        self.__connections.add(conn)
        self.__concount += 1
    
    @property
    def connections(self):
        """
        Retorna as conexões atuais e o contador de conexões.

        Returns
        -------
        tuple
            Uma tupla contendo o conjunto de conexões e o contador de conexões.
        """
        return self.__connections.connections, self.__concount

cliente = Client()