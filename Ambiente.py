from Elemento import Elemento
from typing import List
from Posicao import Posicao
from Acao import Acao, TipoAcao
from Agente import Agente
from Observacao import Observacao
from Farol import Farol
from SensorBussola import SensorBussola
from SensorVisao import SensorVisao

class Ambiente:
    def __init__(self, largura: int, altura: int, elementos: List[Elemento]):
        self.largura = largura
        self.altura = altura
        self.elementos = elementos
        self.posicoes_risco: List[Posicao] = []

    def todos_elementos_posicao(self, pos: Posicao) -> List[Elemento]:
        elementosPosicao: List[Elemento] = []
        for e in self.elementos:
            if e.posicao == pos:
                elementosPosicao.append(e)
        return elementosPosicao

    def agir(self, acao: Acao, agente: Agente) ->float:
        recompensa = 0.0

        if acao.tipo == TipoAcao.MOVER:
            recompensa = -0.1 # recompensa por defeito

            dx = acao.parametros.get('dx', 0)
            dy = acao.parametros.get('dy', 0)

            novo_x = dx + agente.posicao.x
            novo_y = dy + agente.posicao.y
            nova_pos = Posicao(novo_x, novo_y)

            # verificar se não saí dos limites da grelha
            # TODO: REVER PARA CENARIO DE LABIRITNO PORQUE SAIDA VAI SER NAS MARGENS
            if not (0 <= novo_x < self.largura and 0 <= novo_y < self.altura):
                recompensa -= 1.0 # penalidade e não mexe

            # verificar colisões
            elementos_pos = self.todos_elementos_posicao(nova_pos)

            colisao = False
            encontrou_farol = False

            for elem in elementos_pos:
                if elem == agente:
                    continue

                # verificar se é sólido
                if getattr(elem, 'solido', False):
                    colisao = True

                # verificar se é farol
                if isinstance(elem, Farol):
                    encontrou_farol = True

            if colisao:
                recompensa = -5.0
            else:
                # agente move-se
                agente.posicao = nova_pos

                if encontrou_farol:
                    recompensa = 100.0

        elif acao.tipo == TipoAcao.COMUNICAR:
            # avisar que posição é perigosa

            # verificar se a posição já não está na lista
            if agente.posicao not in self.posicoes_risco:
                self.posicoes_risco.append(agente.posicao)

            recompensa = -0.2

        return recompensa

    def observacaoPara(self, agente: Agente) -> Observacao:
        # FAROL
        dados_vetor = None
        dados_vizinhanca = {}

        for sensor in agente.sensores:
            # sensor do farol
            if isinstance(sensor, SensorBussola):
                dados_vetor = sensor.ler(self, agente)

            # sensor do labirinto
            if isinstance(sensor, SensorVisao):
                dados_vizinhanca=sensor.ler(self, agente)

        # LABIRINTO
        # TODO: observacaoPara Labirinto
        return Observacao(
            posicao_agente=agente.posicao,
            vetor_farol=dados_vetor,  # usado no Farol
            vizinhanca=dados_vizinhanca,  # usado no Labirinto
            posicoes_risco=self.posicoes_risco
        )

    def atualizacao(self):
        for elem in self.elementos:
            if hasattr(elem, 'update'):
                elem.update(self)

    def __str__(self):
        grelha = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]

        for e in self.elementos:
            x, y = e.posicao.x, e.posicao.y

            if 0 <= x < self.largura and 0 <= y < self.altura:
                grelha[y][x] = e.simbolo

        return "\n".join(["".join(linha) for linha in grelha])