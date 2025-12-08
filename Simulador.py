from abc import ABC, abstractmethod
from typing import List
from Agente import Agente

class Simulador(ABC):

    @classmethod
    @abstractmethod
    def cria(cls, nome_do_ficheiro_parametros: str) -> 'Simulador':
        pass

    @abstractmethod
    def listaAgentes(self) -> List[Agente]:
        pass

    @abstractmethod
    def executa(self):
        pass