from Elemento import Elemento
from typing import List
from Posicao import Posicao

class Ambiente:
    def __init__(self, largura: int, altura: int, elementos: List[Elemento]):
        self.largura = largura
        self.altura = altura
        self.elementos = elementos

    def remover_elemento(self, elemento: Elemento):
        self.elementos.remove(elemento)

    def todos_elementos_posicao(self, pos: Posicao):
        elementosPosicao: List[Elemento] = []
        for e in self.elementos:
            if e.posicao.posicao_igual(pos):
                elementosPosicao.append(e)
        return elementosPosicao

    def __str__(self):
        return (f"[O ambiente tem {self.largura} de largura, {self.altura} de altura"
                f" e tem os seguintes elementos: {self.elementos}]")