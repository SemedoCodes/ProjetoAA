from Elemento import Elemento
from Posicao import Posicao

class Saida(Elemento):
    def __init__(self, posicao: Posicao):
        super().__init__("Saida", posicao, "S", False)
        self.solido = False