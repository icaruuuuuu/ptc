from logging import *
from datetime import datetime
import os

class Logger:
    """
    Classe responsável por gerenciar o registro de mensagens (logs) em arquivos.

    Esta classe cria um arquivo de log com um nome baseado na data e hora atuais e fornece
    um método para registrar mensagens nesse arquivo.

    Attributes
    ----------
    __name : str
        Nome do arquivo de log, gerado a partir da data e hora atuais no formato `msgs_AAAA-MM-DD_HH-MM-SS`.
    """

    def __init__(self):
        """
        Inicializa o Logger.

        Cria um diretório para armazenar os logs, se não existir, e configura o arquivo de log
        com o nome baseado na data e hora atuais.
        """
        self.__name = datetime.now().strftime('msgs_%Y-%m-%d_%H-%M-%S')
        if not os.path.exists(f'logs/msglogs/'): os.makedirs(f'logs/msglogs/')
        basicConfig(level=INFO,
                    format='%(message)s',
                    filename=f'logs/msglogs/{self.__name}.txt',
                    filemode='w')
    
    def log(self, msg: str):
        """
        Registra uma mensagem no arquivo de log.

        Parameters
        ----------
        msg : str
            A mensagem a ser registrada no arquivo de log.
        """
        info(msg)

logger = Logger()