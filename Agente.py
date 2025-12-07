from abc import ABC, abstractmethod
from Elemento import Elemento
from Posicao import Posicao
from Observacao import Observacao
# from Sensor import Sensor

class Agente(Elemento, ABC):

    def __init__ (self, id_agente: id, posicao: Posicao):
        super().__init__(f"Agente {id_agente}", posicao, "A", True)
        self.id = id_agente

        self.recompensa_acumulada = 0.0
        self.sensores = []  # lista de sensores
        self.politica = None
        self.ultima_observacao = None
        self.ativo = True

    def definir_politica(self, politica):
        self.politica = politica

    def cria(self, nome_do_ficheiro: str):
        pass

    def observacao(self, obs: Observacao):
        self.ultima_observacao = obs

    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def configura_ambiente(self, id_agente: int, posicao: Posicao):
        pass

    def avaliacaoEstadoAtual(self, recompensa: float):
        self.recompensa_acumulada += recompensa

    def instala (self, sensor):
        self.sensores.append(sensor)

    def comunica(self, mensagem: str, de_agente: 'Agente'):
        print(f"[{self.nome}] Recebi: {mensagem}")
