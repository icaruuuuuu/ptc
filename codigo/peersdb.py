from threading import Lock
from utils import *

class PeersDatabase:
    def __init__(self):
        self.peers = set({})
        self.__lock = Lock()
    
    def __str__(self):
        return str(self.peers)
    
    def add(self, peer):
        with self.__lock:
            self.peers.add(peer)

    def multi_add(self, peers:list):
        for peer in peers:
            self.add(peer)
    
    def remove(self, peer):
        with self.__lock:
            if peer in self.peers: self.peers.remove(peer)

peersdb = PeersDatabase()
