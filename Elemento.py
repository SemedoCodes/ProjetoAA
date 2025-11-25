from Posicao import Posicao

class Elemento:
    def __init__(self, nome: str, posicao: Posicao):
        self.nome = nome
        self.posicao = posicao

    def __str__(self):
        return f"[{self.nome}] em {self.posicao}"