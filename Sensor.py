from abc import ABC, abstractmethod

class Sensor(ABC):
    """
    Interface base para sensores.
    """
    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def ler(self, ambiente, agente):
        pass