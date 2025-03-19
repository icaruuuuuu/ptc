from socket import *
import platform

def hostname():
    if platform.system() == 'Linux': return gethostbyname(gethostname() + '.lan')
    if platform.system() == 'Windows': return gethostbyname(gethostname() + '.lan')
    