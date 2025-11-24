class Elemento:
    def __init__(self, nome, posicao):
        self.nome = nome
        self.posicao = posicao


    def getNome(self):
        return self.nome

    def getPosicao(self):
        return self.posicao

    def __str__(self):
        return f"[{self.nome}] em {self.posicao}"