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