from Elemento import Elemento

class Farol (Elemento):
    def __init__(self, posicao):
        super().__init__("Farol", posicao)
        self.solido=False # Agente pode ir para cima do Farol