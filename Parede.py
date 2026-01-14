from Elemento import Elemento
from Posicao import Posicao

class Parede (Elemento):
    def __init__(self, posicao: Posicao):
        super().__init__("Parede", posicao, '#', True)
        self.solido=True