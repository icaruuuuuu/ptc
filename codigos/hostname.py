from socket import *
import platform

def obter_hostname(port):
    if platform.system() == 'Linux': hostname = gethostbyname(gethostname() + '.lan')
    if platform.system() == 'Windows': hostname = gethostbyname(gethostname())
    return hostname + f':{port}'

