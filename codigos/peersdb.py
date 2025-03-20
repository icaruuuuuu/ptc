from threading import Thread, Lock
from time import sleep
from qol import *

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
if __name__ == '__main__':
    def thread_func():
        global peersdb
        for i in range(5):
            peersdb.update(f'{i}.{i}.{i}.{i}:{i}')
            print(peersdb)


    Thread(target=thread_func).start()
    Thread(target=thread_func).start()
    Thread(target=thread_func).start()
    Thread(target=thread_func).start()
    Thread(target=thread_func).start()

