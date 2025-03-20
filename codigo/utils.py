from socket import *
import platform
def obter_hostname(port):
    if platform.system() == 'Linux': hostname = get_local_ip_linux()
    if platform.system() == 'Windows': hostname = gethostbyname(gethostname())
    return hostname + f':{port}'

def tuple_to_socket(addr: tuple) -> str:
    return f'{addr[0]}:{addr[1]}'

def socket_to_tuple(s: str) -> tuple:
    aux = s.split(':')
    addr = (aux[0], int(aux[1]))
    return addr

def peers_to_str(hostname:str, peers:set):
    r = hostname
    for p in peers: r += ' ' + p
    return r

import subprocess

def get_local_ip_linux():
    try:
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "inet " in line and "127.0.0.1" not in line:
                    return line.split()[1].split('/')[0]
        return None
    except Exception as e:
        print(f"Erro ao obter o IP local: {e}")
        return None