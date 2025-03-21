import json
import os
import hashlib

def criptografar(senha: str) -> str:
    """
    Criptografa uma senha usando o algoritmo SHA-256.

    Parameters
    ----------
    senha : str
        A senha a ser criptografada.

    Returns
    -------
    str
        A senha criptografada em formato hexadecimal.
    """
    hash_object = hashlib.sha256()
    hash_object.update(senha.encode('utf-8'))
    return hash_object.hexdigest()

class UserException(Exception):
    """
    Exceção personalizada para erros relacionados ao usuário.

    Esta exceção é levantada quando ocorre um erro específico relacionado às operações do usuário,
    como senha incorreta ou senha não confirmada.
    """
    ...

class User:
    """
    Classe responsável por gerenciar as informações e operações do usuário.

    Esta classe lida com o cadastro (signin) e login do usuário, além de armazenar as credenciais
    em um arquivo JSON.

    Attributes
    ----------
    __name : str
        Nome do usuário.
    __password : str
        Senha criptografada do usuário.
    """

    def __init__(self):
        """
        Inicializa o usuário. Se o arquivo de credenciais existir, carrega as informações.
        Caso contrário, inicia o processo de cadastro (signin).
        """
        self.__name = ''
        self.__password = ''
        if os.path.exists('userinfo/user.json'):
            with open('userinfo/user.json', 'r') as file: credentials = json.load(file)
            self.__name = credentials['username']
            self.__password = credentials['password']
        else:
            print('<SISTEMA>: Credenciais de login não encontradas.')
            self.signin()
            
    def __str__(self) -> str:
        """
        Retorna o nome do usuário.

        Returns
        -------
        str
            O nome do usuário.
        """
        return self.__name
    
    def signin(self):
        """
        Realiza o cadastro de um novo usuário.

        O usuário é solicitado a fornecer um nome de usuário e uma senha. A senha é confirmada
        e, se válida, criptografada e armazenada junto com o nome do usuário em um arquivo JSON.
        """
        self.__name = input('<SISTEMA>: Novo nome de usuário: ')
        while True:
            try:
                self.__password = input('<SISTEMA>: Senha do usuário: ')
                confirm = input('<SISTEMA>: Confirme a senha do usuário: ')
                if self.__password != confirm: raise UserException('Senha não confirmada')
                break
            except UserException as e: 
                print(f'<SISTEMA>: {e}')

        self.__password = criptografar(self.__password)
        credentials = {
            'username': self.__name,
            'password': self.__password
        }
        with open('userinfo/user.json', 'w') as file:
            json.dump(credentials, file)
    
    def login(self):
        """
        Realiza o login do usuário.

        O usuário é solicitado a fornecer a senha. Se a senha estiver correta, o login é bem-sucedido.
        Caso contrário, uma exceção é levantada.

        Raises
        ------
        UserException
            Se a senha fornecida estiver incorreta.
        """
        while True:
            try:
                password = criptografar(input('Senha: '))
                criptografar(self.__password)
                if password != self.__password: raise UserException('Senha incorreta.')
                break
            except UserException as e:
                print(f'<SISTEMA>: {e}')