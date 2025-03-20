from socket import *
from threading import Thread
from peersdb import peersdb
from client import *
from utils import *

class Server:
    def __init__(self, port, client:Client):
        self.__port = port
        self.__server = socket(AF_INET, SOCK_STREAM)
        self.__server.bind(('0.0.0.0', port))
        self.__server.listen(100)

        self.__threads : list[Thread] = []
        self.__client = client

    def start(self):
        global peersdb
        global cliente
        print('Iniciando servidor...')
        try:
            while True:
                conn, addr = self.__server.accept()
                data = conn.recv(4096).decode('utf-8')
                # print(data)

                for p in data.split(): 
                    if p != obter_hostname(self.__port) and p not in peersdb.peers: 
                        cliente.connect(socket_to_tuple(p), obter_hostname(self.__port))
                        peersdb.add(p)

                thread = Thread(target=self.handle_peer, args=(conn, addr))
                self.__threads.append(thread)
                thread.start()
        except Exception as e: print(f'Erro no servidor. {e}')
        finally: self.finish()

    def handle_peer(self, conn:socket, addr:tuple):
        # print(f'Conexão aceita com {tuple_to_socket(addr)}')

        try:
            while True:
                data = conn.recv(4096)
                if not data or data.strip() == '': break

                msg = data.decode('utf-8')
                print(f'{msg}')
        except Exception as e:
            print(f'Erro ao tratar conexão com {addr}: {e}')
        finally:
            conn.close()
            peersdb.remove(tuple_to_socket(addr))
    
    def finish(self):
        self.__server.close()
        for thread in self.__threads:
            thread.join()
