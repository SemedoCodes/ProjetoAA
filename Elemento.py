from Posicao import Posicao

class Elemento:
    """
    Classe base para todos os objetos na grelha (Paredes, Agentes, Farol, etc).
    """
    def __init__(self, nome: str, posicao: Posicao, simbolo: str, solido: bool):
        self.nome = nome
        self.posicao = posicao
        self.simbolo = simbolo
        self.solido = solido # se true, causa colisão

    # Método para elementos dinâmicos
    def update(self, ambiente):
        pass

    def __str__(self):
        return f"[{self.nome}] em {self.posicao}"