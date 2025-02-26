import json
from socket import *

# Configuração do socket
PORTA = int(input('Digite uma porta para escuta: '))
node = socket(AF_INET, SOCK_STREAM)
node.bind(('0.0.0.0', PORTA))

# Conecta ao peer remoto
addr = ('127.0.0.1', int(input('Digite uma porta para envio: ')))
node.connect(addr)

# Lista de peers inicial
peers = ['10.0.0.1:5000', '10.0.0.2:5000', '10.0.0.3:5000']
print(f"Peers iniciais: {peers}")

# Envia a lista de peers
compat = json.dumps(peers)
node.sendall(compat.encode('utf-8'))

# Recebe a lista de peers do peer remoto
data = node.recv(4096)
novos_peers = json.loads(data.decode('utf-8'))

# Combina as listas de peers
peers = list(set(peers + novos_peers))
print(f"Lista de peers atualizada: {peers}")

# Fecha a conexão
node.close()