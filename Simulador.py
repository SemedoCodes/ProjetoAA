from abc import ABC, abstractmethod
from typing import List
from Agente import Agente

class Simulador(ABC):
    """
    Interface abstrata para o Motor de Simulação.
    """
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