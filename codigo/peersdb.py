from threading import Lock
from utils import *

class PeersDatabase:
    """
    Uma classe para gerenciar um banco de dados de peers (nós) em uma rede P2P.

    Esta classe utiliza um conjunto (set) para armazenar os peers e um Lock para garantir
    operações thread-safe ao adicionar ou remover peers.

    Attributes
    ----------
    peers : set
        Um conjunto que armazena os endereços dos peers.
    __lock : threading.Lock
        Um Lock para garantir operações thread-safe.

    Methods
    -------
    __str__()
        Retorna uma representação em string do conjunto de peers.
    add(peer)
        Adiciona um peer ao banco de dados.
    multi_add(peers)
        Adiciona múltiplos peers ao banco de dados.
    remove(peer)
        Remove um peer do banco de dados.
    """

    def __init__(self):
        """
        Inicializa o banco de dados de peers.

        Cria um conjunto vazio para armazenar os peers e um Lock para garantir
        operações thread-safe.
        """
        self.peers = set({})
        self.__lock = Lock()
    
    def __str__(self):
        """
        Retorna uma representação em string do conjunto de peers.

        Returns
        -------
        str
            Uma string representando o conjunto de peers.
        """
        return str(self.peers)
    
    def add(self, peer):
        """
        Adiciona um peer ao banco de dados.

        Parameters
        ----------
        peer : str
            O endereço do peer a ser adicionado (ex: "192.168.1.1:5000").
        """
        with self.__lock:
            self.peers.add(peer)

    def multi_add(self, peers: list):
        """
        Adiciona múltiplos peers ao banco de dados.

        Parameters
        ----------
        peers : list of str
            Uma lista de endereços de peers a serem adicionados.
        """
        for peer in peers:
            self.add(peer)
    
    def remove(self, peer):
        """
        Remove um peer do banco de dados.

        Parameters
        ----------
        peer : str
            O endereço do peer a ser removido (ex: "192.168.1.1:5000").
        """
        with self.__lock:
            if peer in self.peers:
                self.peers.remove(peer)

# Instância global do banco de dados de peers
peersdb = PeersDatabase()