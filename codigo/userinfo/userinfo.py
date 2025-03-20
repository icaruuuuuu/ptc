import json
import os
import hashlib

def criptografar(senha):
    hash_object = hashlib.sha256()
    hash_object.update(senha.encode('utf-8'))
    return hash_object.hexdigest()

class UserException(Exception):
    ...

class User():
    def __init__(self):
        self.__name = ''
        self.__password = ''
        if os.path.exists('userinfo/user.json'):
            with open('userinfo/user.json', 'r') as file: credentials = json.load(file)
            self.__name = credentials['username']
            self.__password = credentials['password']
        else:
            print('<SISTEMA>: Credenciais de login não encontradas.')
            self.signin()
            
    def __str__(self):
        return self.__name
    
    def signin(self):
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
        while True:
            try:
                password = criptografar(input('Senha: '))
                criptografar(self.__password)
                if password != self.__password: raise UserException('Senha incorreta.')
                break
            except UserException as e:
                print(f'<SISTEMA>: {e}')

