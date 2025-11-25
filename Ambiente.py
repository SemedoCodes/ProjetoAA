from Elemento import Elemento
from typing import List
from Posicao import Posicao
from Acao import Acao, TipoAcao
from Agente import Agente
from Observacao import Observacao
from Farol import Farol

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

    def agir(self, acao: Acao, agente: Agente):
        if acao.tipo == TipoAcao.MOVER:
            recompensa = -0.1 # recompensa por defeito (custo de movimento)

            dx = acao.parametros.get('dx', 0)
            dy = acao.parametros.get('dy', 0)

            novo_x = dx + agente.posicao.x
            novo_y = dy + agente.posicao.y

            nova_pos = Posicao(novo_x, novo_y)

            # verificar se não saí dos limites da grelha
            # TODO: REVER PARA CENARIO DE LABIRITNO PORQUE SAIDA VAI SER NAS MARGENS
            if not (0 < novo_x < self.largura and 0 < novo_y < self.altura):
                recompensa -= 1.0

            # verificar colisões
            elementos_pos = self.todos_elementos_posicao(nova_pos)
            if elementos_pos[0].solido == True:
                if not isinstance(elementos_pos[0], Agente):
                    recompensa -= 5.0
                return

            # TODO: INCLUIR LABIRINTO
            if isinstance(elementos_pos[0], Farol):
                recompensa +=100.0

            # mover agente
            agente.posicao = nova_pos
        return

    def observacaoPara(self, agente: Agente):
        return #Observaca

    def atualizacao(self):
        return

    def __str__(self):
        grelha = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]

        for e in self.elementos:
            x, y = e.posicao.x, e.posicao.y

            if 0 <= x < self.largura and 0 <= y < self.altura:
                grelha[y][x] = e.simbolo

        return "\n".join(["".join(linha) for linha in grelha])