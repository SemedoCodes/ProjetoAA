from Elemento import Elemento
from Posicao import Posicao

class Obstaculo (Elemento):
    def __init__(self, posicao: Posicao):
        super().__init__("Obstáculo", posicao, 'O')
        self.solido=True