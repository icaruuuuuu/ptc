from socket import *
from threading import Thread
from peersdb import peersdb
from client import *
from utils import *
from logs.logger import logger

class Server:
    """
    Uma classe que implementa um servidor para comunicação P2P.

    Este servidor aceita conexões de peers, gerencia threads para cada conexão e
    facilita a troca de mensagens entre os peers. Ele também atualiza dinamicamente
    a lista de peers conectados.

    Attributes
    ----------
    __port : int
        A porta na qual o servidor escuta conexões.
    __server : socket
        O socket do servidor.
    __threads : list[Thread]
        Uma lista de threads que gerenciam conexões com peers.
    __client : Client
        Uma instância do cliente associado ao servidor.

    Methods
    -------
    start()
        Inicia o servidor e começa a aceitar conexões de peers.
    handle_peer(conn, addr)
        Gerencia a comunicação com um peer conectado.
    finish()
        Finaliza o servidor, fechando todas as conexões e threads.
    """

    def __init__(self, port, client: Client):
        """
        Inicializa o servidor com a porta e o cliente especificados.

        Parameters
        ----------
        port : int
            A porta na qual o servidor escutará conexões.
        client : Client
            Uma instância do cliente associado ao servidor.
        """
        self.__port = port
        self.__server = socket(AF_INET, SOCK_STREAM)
        self.__server.bind(('0.0.0.0', port))
        self.__server.listen(100)

        self.__threads: list[Thread] = []
        self.__client = client

    def start(self):
        """
        Inicia o servidor e começa a aceitar conexões de peers.

        O servidor escuta indefinidamente por novas conexões. Quando uma conexão é
        estabelecida, ele cria uma nova thread para gerenciar a comunicação com o peer
        e atualiza a lista de peers conectados.
        """
        global peersdb
        global cliente
        print('<SISTEMA>: Iniciando servidor...')
        try:
            while True:
                conn, addr = self.__server.accept()
                data = conn.recv(4096).decode('utf-8')

                # Processa os peers recebidos e adiciona à lista de peers
                for p in data.split():
                    if p != obter_hostname(self.__port) and p not in peersdb.peers:
                        cliente.connect(socket_to_tuple(p), obter_hostname(self.__port))
                        peersdb.add(p)

                # Cria uma nova thread para gerenciar a conexão com o peer
                thread = Thread(target=self.handle_peer, args=(conn, addr))
                self.__threads.append(thread)
                thread.start()
        except Exception as e:
            print(f'<SISTEMA>: Erro no servidor. {e}')
        finally:
            self.finish()

    def handle_peer(self, conn: socket, addr: tuple):
        """
        Gerencia a comunicação com um peer conectado.

        Este método é executado em uma thread separada para cada peer. Ele recebe
        mensagens do peer e as exibe no console, além de registrá-las no logger.

        Parameters
        ----------
        conn : socket
            O socket da conexão com o peer.
        addr : tuple
            O endereço (IP, porta) do peer.
        """
        try:
            while True:
                data = conn.recv(4096)
                if not data or data.strip() == '':
                    break

                # Exibe e registra a mensagem recebida
                msg = data.decode('utf-8')
                print(f'{msg}')
                logger.log(msg)
        except Exception as e:
            print(f'<SISTEMA>: Erro ao tratar conexão com {addr}: {e}')
        finally:
            conn.close()
            peersdb.remove(tuple_to_socket(addr))

    def finish(self):
        """
        Finaliza o servidor, fechando todas as conexões e threads.

        Este método fecha o socket do servidor e aguarda a finalização de todas as
        threads que gerenciam conexões com peers.
        """
        self.__server.close()
        for thread in self.__threads:
            thread.join()