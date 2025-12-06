from abc import ABC, abstractmethod
# from Ambiente import Ambiente
# from Agente import Agente

class Sensor(ABC):
    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def ler(self, ambiente, agente):
        """
        Recebe o ambiente e o agente.
        """
        pass