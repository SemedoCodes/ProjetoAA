from Elemento import Elemento
from typing import List
from Posicao import Posicao

class Ambiente:
    def __init__(self, largura: int, altura: int, elementos: List[Elemento]):
        self.largura = largura
        self.altura = altura
        self.elementos = elementos

    def todos_elementos_posicao(self, pos: Posicao):
        elementosPosicao: List[Elemento] = []
        for e in self.elementos:
            if e.posicao.posicao_igual(pos):
                elementosPosicao.append(e)
        return elementosPosicao

    def __str__(self):
        grelha = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]

        for e in self.elementos:
            x, y = e.posicao.x, e.posicao.y

            if 0 <= x < self.largura and 0 <= y < self.altura:
                grelha[y][x] = e.simbolo

        return "\n".join(["".join(linha) for linha in grelha])