from server import *
from client import *
from utils import obter_hostname
from peersdb import peersdb
from userinfo.userinfo import User, UserException
from logs.logger import logger

# Criando uma instância do usuário e realiza o login
usuario = User()
usuario.login()

# Solicitando ao usuário que insira a porta fixa para comunicação
PORTA = int(input('<SISTEMA>: Digite a porta fixa de comunicação: '))

# Iniciando o servidor em uma thread separada com a porta especificada
servidor = Server(PORTA, cliente)
Thread(target=servidor.start, daemon=True).start()

# Dicionário de comandos disponíveis para o usuário
comandos = {
    '/connect': lambda e : cliente.connect(socket_to_tuple(e.split()[1]), obter_hostname(PORTA)),  # Conecta a um peer. Parâmetro do comando é um par IP:PORTA (Ex.: 192.168.0.50:5000)
    '/peers' : lambda e : print(peersdb.peers),  # Exibe a lista de peers conhecidos
    '/connections' : lambda e : print(cliente.connections),  # Exibe as conexões ativas
    '/resignin': lambda e : usuario.signin()  # Permite ao usuário redefinir suas credenciais
}

if __name__ == '__main__':
    while True:
        # Solicitando uma entrada não vazia do usuário
        e = input()
        if e == '': continue
        
        # Verificando se a entrada é um comando (começa com '/')
        if e[0] == '/': 
            try:
                # Executando o comando correspondente
                comandos[e.split()[0]](e)
            except Exception as e:
                # Exibe uma mensagem de erro se o comando falhar
                print(f'<SISTEMA>: Erro ao executar comando: {e}')
        else:
            # Se não for um comando, envia a mensagem para todos os peers conectados e a registra no log
            cliente.send_msg(f'<{usuario}>: {e}')
            logger.log(f'<{usuario}>: {e}')