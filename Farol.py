from Elemento import Elemento
from Posicao import Posicao

class Farol (Elemento):
    def __init__(self, posicao: Posicao):
        super().__init__("Farol", posicao, 'F', True)
        self.solido=False # agente pode ir para cima do Farol