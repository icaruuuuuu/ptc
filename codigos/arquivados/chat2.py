import socket
import threading
import json

# Função para tratar conexões de peers (lado servidor)
def handle_peer_connection(conn, addr):
    try:
        data = conn.recv(4096)
        if data:
            # Decodifica a mensagem (supondo formato JSON)
            mensagem = json.loads(data.decode('utf-8'))
            print(f"\nMensagem recebida de {addr}: {mensagem.get('texto')}")
    except Exception as e:
        print(f"Erro ao tratar conexão de {addr}: {e}")
    finally:
        conn.close()

# Thread que fica escutando por novas conexões
def iniciar_servidor(porta):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', porta))
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
        cliente.send(json.dumps(mensagem).encode('utf-8'))
        print(f"Mensagem enviada para {ip_peer}:{porta_peer}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {ip_peer}:{porta_peer} -> {e}")
    finally:
        cliente.close()

if __name__ == '__main__':
    minha_porta = int(input("Digite a porta para escutar mensagens: "))
   
    # Inicia o servidor em uma thread separada
    threading.Thread(target=iniciar_servidor, args=(minha_porta,), daemon=True).start()

    # Defina os dados do peer que você irá enviar as mensagens
    print("\nDefina o IP e a porta do peer para enviar mensagens:")
    ip_peer = input("  IP do peer: ")
    porta_peer = int(input("  Porta do peer: "))

    # Loop principal para enviar mensagens
    while True:
        texto = input("Digite a mensagem: ")
        enviar_mensagem(ip_peer, porta_peer, texto)

