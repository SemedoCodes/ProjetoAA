from Elemento import Elemento
from Posicao import Posicao

# Consideramos Parede filha de elemento ou filha de obstáculo?
class Parede (Elemento):
    def __init__(self, posicao: Posicao):
        super().__init__("Parede", posicao, '#')
        self.solido=True