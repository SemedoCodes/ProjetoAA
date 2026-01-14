from Elemento import Elemento
from typing import List, Tuple, Dict
from Posicao import Posicao
from Accao import Accao, TipoAccao
from Agente import Agente
from Observacao import Observacao
from Farol import Farol
from Saida import Saida
from SensorBussola import SensorBussola
from SensorVisao import SensorVisao
import threading

class Ambiente:
    """
    Representa o mundo físico da simulação.
    Gere colisões, movimentos e validação de regras.
    """
    def __init__(self, largura: int, altura: int, elementos: List[Elemento]):
        self.largura = largura
        self.altura = altura
        self.elementos = elementos
        self.posicoes_risco: List[Posicao] = []
        self.rasto: Dict[Tuple[int, int], str] = {}
        self.lock = threading.RLock()

    def todos_elementos_posicao(self, pos: Posicao) -> List[Elemento]:
        elementosPosicao: List[Elemento] = []
        for e in self.elementos:
            if e.posicao == pos: elementosPosicao.append(e)
        return elementosPosicao

    # Executa uma ação no mundo e devolve a recompensa (extrínseca)
    def agir(self, acao: Accao, agente: Agente) ->float:
        with self.lock:
            recompensa = 0.0

            if acao.tipo == TipoAccao.MOVER:
                dx = acao.parametros.get('dx', 0)
                dy = acao.parametros.get('dy', 0)

                # Calcular nova potencial posição
                novo_x = dx + agente.posicao.x
                novo_y = dy + agente.posicao.y
                nova_pos = Posicao(novo_x, novo_y)

                # Verificar limites do mapa
                if not (0 <= novo_x < self.largura and 0 <= novo_y < self.altura):
                    recompensa -= 0.5 # penalidade por movimento inválido
                    return recompensa

                # Verificar colisões
                elementos_pos = self.todos_elementos_posicao(nova_pos)
                colisao = False
                encontrou_objetivo = False

                for elem in elementos_pos:
                    if elem == agente:
                        continue

                    if getattr(elem, 'solido', False):
                        colisao = True

                    if isinstance(elem, Farol) or isinstance(elem, Saida):
                        encontrou_objetivo = True

                if colisao:
                    recompensa -= 10.0 # penalidade por colisão
                else:
                    # Atualizar rasto visual
                    simbolo = '_' if dx != 0 else '|'
                    self.rasto[(agente.posicao.x, agente.posicao.y)] = simbolo

                    agente.posicao = nova_pos

                    if encontrou_objetivo:
                        recompensa += 100.0 # recompensa por atingir o objetivo

            elif acao.tipo == TipoAccao.COMUNICAR:
                mensagem = acao.parametros.get('msg', "")

                # Entregar a mensagem a todos os outros agentes
                for elem in self.elementos:
                    if isinstance(elem, Agente) and elem.id != agente.id:
                        elem.comunica(mensagem, agente)

            return recompensa

    # Gera a observação baseada nos sensores instalados no agente
    def observacaoPara(self, agente: Agente) -> Observacao:
        with self.lock:
            dados_vetor = None
            dados_vizinhanca = {}

            for sensor in agente.sensores:
                if isinstance(sensor, SensorBussola):
                    dados_vetor = sensor.ler(self, agente)
                if isinstance(sensor, SensorVisao):
                    dados_vizinhanca=sensor.ler(self, agente)

            return Observacao(
                posicao_agente=agente.posicao,
                vetor_farol=dados_vetor,  # usado no Farol
                vizinhanca=dados_vizinhanca,  # usado no Labirinto
                posicoes_risco=self.posicoes_risco
            )

    # Atualiza os elementos dinâmicos
    def atualizacao(self):
        for elem in self.elementos:
            if hasattr(elem, 'update'):
                elem.update(self)

    # Desenha a grelha
    def __str__(self):
        grelha = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]
        agentes_para_desenhar = []

        for (rx, ry), simbolo in self.rasto.items():
            if 0 <= rx < self.largura and 0 <= ry < self.altura:
                grelha[ry][rx] = simbolo

        for e in self.elementos:
            if isinstance(e, Agente):
                agentes_para_desenhar.append(e)
            x, y = e.posicao.x, e.posicao.y

            if 0 <= x < self.largura and 0 <= y < self.altura:
                grelha[y][x] = e.simbolo

        for a in agentes_para_desenhar:
            x, y = a.posicao.x, a.posicao.y
            if 0 <= x < self.largura and 0 <= y < self.altura:
                grelha[y][x] = a.simbolo

        return "\n".join(["".join(linha) for linha in grelha])