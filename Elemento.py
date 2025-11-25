from Posicao import Posicao

class Elemento:
    def __init__(self, nome: str, posicao: Posicao, simbolo: str):
        self.nome = nome
        self.posicao = posicao
        self.simbolo = simbolo

    def __str__(self):
        return f"[{self.nome}] em {self.posicao}"