import socket
import threading
import json
import os

# Nome do arquivo que armazena os peers conhecidos
ARQUIVO_PEERS = "peers.json"

# Carregar ou criar lista de peers
def carregar_peers():
    if os.path.exists(ARQUIVO_PEERS):
        with open(ARQUIVO_PEERS, "r") as file:
            return json.load(file)
    return []

# Salvar lista de peers
def salvar_peers(peers):
    with open(ARQUIVO_PEERS, "w") as file:
        json.dump(peers, file, indent=4)

# Função para tratar conexões de peers
def handle_peer_connection(conn, addr):
    try:
        data = conn.recv(4096)
        if data:
            mensagem = json.loads(data.decode("utf-8"))
            print(f"\nMensagem recebida de {addr}: {mensagem.get('texto')}")
    except Exception as e:
        print(f"Erro ao tratar conexão de {addr}: {e}")
    finally:
        conn.close()

# Thread para escutar conexões
def iniciar_servidor(porta):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", porta))
    servidor.listen(5)
    print(f"Servidor ativo na porta {porta}. Aguardando conexões...")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=handle_peer_connection, args=(conexao, endereco), daemon=True).start()

# Função para enviar mensagem a um peer específico
def enviar_mensagem(ip_peer, porta_peer, texto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((ip_peer, porta_peer))
        mensagem = {"texto": texto}
        cliente.send(json.dumps(mensagem).encode("utf-8"))
        print(f"Mensagem enviada para {ip_peer}:{porta_peer}")

        # Adiciona o peer à lista se ainda não estiver salvo
        peers = carregar_peers()
        if {"ip": ip_peer, "porta": porta_peer} not in peers:
            peers.append({"ip": ip_peer, "porta": porta_peer})
            salvar_peers(peers)

    except Exception as e:
        print(f"Erro ao enviar mensagem para {ip_peer}:{porta_peer} -> {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    minha_porta = int(input("Digite a porta para escutar mensagens: "))

    # Inicia o servidor em uma thread separada
    threading.Thread(target=iniciar_servidor, args=(minha_porta,), daemon=True).start()

    while True:
        peers = carregar_peers()

        # Exibir peers conhecidos
        if peers:
            print("\nPeers conhecidos:")
            for i, peer in enumerate(peers, 1):
                print(f"{i}. {peer['ip']}:{peer['porta']}")
            print(f"{len(peers) + 1}. Digitar novo peer")

            opcao = int(input("\nEscolha um peer ou digite um novo: "))
            if opcao <= len(peers):
                ip = peers[opcao - 1]["ip"]
                porta = peers[opcao - 1]["porta"]
            else:
                ip = input("  IP do peer: ")
                porta = int(input("  Porta do peer: "))
        else:
            ip = input("  IP do peer: ")
            porta = int(input("  Porta do peer: "))

        texto = input("Digite a mensagem: ")
        enviar_mensagem(ip, porta, texto)
