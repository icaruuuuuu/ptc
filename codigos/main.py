from server import *
from client import *
from peersdb import peersdb
from hostname import obter_hostname
PORTA = int(input('Digite uma porta: '))

servidor = Server(PORTA, cliente)
Thread(target=servidor.start, daemon=True).start()

comandos = {
    '/connect': lambda e : cliente.connect(socket_to_tuple(e.split()[1]), obter_hostname(PORTA)),
    '/peers' : lambda e : print(peersdb.peers),
    '/connections' : lambda e : print(cliente.connections),
    '/dev' : lambda e : cliente.connections.add(e.split()[1]),
}

if __name__ == '__main__':
    while True:
        e = input()
        if e == '': continue
        if e[0] == '/': 
            try: comandos[e.split()[0]](e)
            except Exception as e: print(f'Erro ao executar comando: {e}')
        else: cliente.send_msg(e)
        


