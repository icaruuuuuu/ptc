from socket import *
import platform
import subprocess

def obter_hostname(port: int) -> str:
    """
    Obtém o endereço IP do host local e o combina com a porta fornecida.

    Parameters
    ----------
    port : int
        A porta que será combinada com o endereço IP.

    Returns
    -------
    str
        O endereço IP do host local seguido da porta no formato `IP:porta`.

    Notes
    -----
    - No Linux, o IP é obtido usando o comando `ip addr`.
    - No Windows, o IP é obtido usando `gethostbyname(gethostname())`.
    """
    if platform.system() == 'Linux': hostname = get_local_ip_linux()
    if platform.system() == 'Windows': hostname = gethostbyname(gethostname())
    return hostname + f':{port}'

def tuple_to_socket(addr: tuple) -> str:
    """
    Converte uma tupla de endereço (IP, porta) em uma string no formato `IP:porta`.

    Parameters
    ----------
    addr : tuple
        Tupla contendo o endereço IP e a porta.

    Returns
    -------
    str
        O endereço no formato `IP:porta`.
    """
    return f'{addr[0]}:{addr[1]}'

def socket_to_tuple(s: str) -> tuple:
    """
    Converte uma string no formato `IP:porta` em uma tupla de endereço (IP, porta).

    Parameters
    ----------
    s : str
        String no formato `IP:porta`.

    Returns
    -------
    tuple
        Tupla contendo o endereço IP e a porta.
    """
    aux = s.split(':')
    addr = (aux[0], int(aux[1]))
    return addr

def peers_to_str(hostname: str, peers: set) -> str:
    """
    Converte um conjunto de peers em uma string formatada.

    Parameters
    ----------
    hostname : str
        O nome do host local.
    peers : set
        Conjunto de peers no formato `IP:porta`.

    Returns
    -------
    str
        String formatada contendo o hostname seguido dos peers, separados por espaços.
    """
    r = hostname
    for p in peers: r += ' ' + p
    return r

def get_local_ip_linux() -> str:
    """
    Obtém o endereço IP local em sistemas Linux.

    Returns
    -------
    str
        O endereço IP local.

    Notes
    -----
    - Utiliza o comando `ip addr` para obter o IP.
    - Ignora o endereço de loopback (`127.0.0.1`).

    Raises
    ------
    Exception
        Se ocorrer um erro ao tentar obter o IP.
    """
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