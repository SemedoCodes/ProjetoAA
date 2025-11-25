from Posicao import Posicao

class Elemento:
    def __init__(self, nome: str, posicao: Posicao, simbolo: str, solido: bool):
        self.nome = nome
        self.posicao = posicao
        self.simbolo = simbolo
        self.solido = solido

    def __str__(self):
        return f"[{self.nome}] em {self.posicao}"