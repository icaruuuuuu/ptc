from logging import *
from datetime import datetime
import os

class Logger:
    def __init__(self):
        self.__name = datetime.now().strftime('msgs_%Y-%m-%d_%H-%M-%S')
        if not os.path.exists(f'logs/msglogs/'): os.makedirs(f'logs/msglogs/')
        basicConfig(level=INFO,
                    format='%(message)s',
                    filename=f'logs/msglogs/{self.__name}.txt',
                    filemode='w')
    
    def log(self,msg):
        info(msg)

logger = Logger()