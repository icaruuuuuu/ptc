import json
from socket import *

# Configuração do socket
PORTA = int(input('Digite uma porta para escuta: '))
node = socket(AF_INET, SOCK_STREAM)
node.bind(('0.0.0.0', PORTA))
node.listen(5)

# Aceita uma conexão
print("Aguardando conexão...")
conn, addr = node.accept()
print(f"Conexão estabelecida com {addr}")

# Lista de peers inicial
peers = ['10.0.0.6:5000', '10.0.0.5:5000', '10.0.0.4:5000']
print(f"Peers iniciais: {peers}")

# Recebe a lista de peers do peer remoto
data = conn.recv(4096)
novos_peers = json.loads(data.decode('utf-8'))

# Envia a lista de peers
compat = json.dumps(peers)
conn.sendall(compat.encode('utf-8'))

# Combina as listas de peers
peers = list(set(peers + novos_peers))
print(f"Lista de peers atualizada: {peers}")

# Fecha a conexão
conn.close()
node.close()