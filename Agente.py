from abc import ABC, abstractmethod
from typing import Any
import Sensor
import Agente
import Posicao

class Agente(ABC):


    def cria(self, nome_do_ficheiro: str):

        pass

    def observacao(sefl, obs: Any):
        pass

    def age(self):
        pass
    
    def avaliacaoEstadoAtual(self, recompensa: float):
        pass

    def instala (sensor: Sensor):
        pass

    def comunica(mensagem: str, de_agente: Agente):
        pass
