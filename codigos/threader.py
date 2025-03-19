from threading import Thread, Lock
from time import sleep

class PeersDatabase:
    def __init__(self):
        self.peers = set()
        self.__lock = Lock()
    
    def __str__(self):
        return str(self.peers)
    
    def update(self, peer):
        with self.__lock:
            self.peers.add(peer)

pdb = PeersDatabase()
def thread_func():
    global pdb
    for i in range(5):
        pdb.update(f'{i}.{i}.{i}.{i}:{i}')
        print(pdb)


Thread(target=thread_func).start()
Thread(target=thread_func).start()
Thread(target=thread_func).start()
Thread(target=thread_func).start()
Thread(target=thread_func).start()

sleep(1)
for p in pdb.peers:
    print(p)