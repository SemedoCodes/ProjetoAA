from Posicao import Posicao
from Elemento import Elemento

class Agente(Elemento):
    def __init__(self, passos_max: int, posicao: Posicao):
        super().__init__("Agente", posicao, 'A')
        self.passos_max = passos_max