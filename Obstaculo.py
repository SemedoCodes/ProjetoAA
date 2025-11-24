from Elemento import Elemento

class Obstaculo (Elemento):
    def __init__(self, posicao):
        super().__init__("Obstáculo", posicao)
        self.solido=True