class Posicao:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Comparar duas posições
    def posicaoIgual (self, p):
        if isinstance(p, Posicao):
            return self.x == p.x and self.y == p.y
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"