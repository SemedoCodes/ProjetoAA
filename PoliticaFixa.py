from Politica import Politica
from Observacao import Observacao
from Accao import Accao, TipoAccao
from typing import Dict, Any, Tuple
import random

class PoliticaFixa(Politica):
    # política de agente com regras fixas/determinísticas.
    # usado para o Modo de Teste ou agentes que não aprendem.

    def __init__(self):
        self.regras_fixas = {}
        self.nome = "Política Fixa"
        self.ultima_posicao = None

    def carregar_politica(self, ficheiro: str):
        # carrega a Q-Table de um ficheiro txt
        self.q_table = {}
        try:
            with open(ficheiro, "r") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    x_str, y_str, acao, q_str = linha.split(",")
                    estado = (int(x_str), int(y_str))
                    q = float(q_str)
                    self.q_table[(estado, acao)] = q
        except FileNotFoundError:
            print(f"AVISO: Ficheiro '{ficheiro}' não encontrado. A usar regras manuais.")

    def selecionar_acao(self, obs) -> Accao:
        estado_atual = (obs.posicao.x, obs.posicao.y)
        acao_teste = self.selecionar_acao_ficheiro(estado_atual)
        if acao_teste:
            return acao_teste

        if obs.tem_vetor():

            colisao = False
            if self.ultima_posicao is not None and self.ultima_posicao == estado_atual:
                colisao = True

            self.ultima_posicao = estado_atual
            dx_total, dy_total = obs.vetor_farol
            if colisao:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                if dx == 0 and dy == 0: dx = 1
                return Accao.mover(dx, dy)

            # se ambos forem 0, estamos em cima do farol
            if dx_total == 0 and dy_total == 0:
                return Accao(TipoAccao.FAZER_NADA)

            # se a distância horizontal for maior ou igual à vertical -> move em X
            if abs(dx_total) >= abs(dy_total):
                if dx_total > 0:
                    return Accao.mover(1, 0)  # Mover Este
                else:
                    return Accao.mover(-1, 0)  # Mover Oeste

            # mover em Y
            else:
                if dy_total > 0:
                    return Accao.mover(0, 1)  # Mover Sul
                else:
                    return Accao.mover(0, -1)  # Mover Norte
        else:
            possiveis = []
            if obs.ver_direcao("Norte") == "Saida": return Accao.mover(0, -1)
            if obs.ver_direcao("Sul") == "Saida":   return Accao.mover(0, 1)
            if obs.ver_direcao("Este") == "Saida":  return Accao.mover(1, 0)
            if obs.ver_direcao("Oeste") == "Saida": return Accao.mover(-1, 0)

            if obs.ver_direcao("Norte") == "Vazio": possiveis.append((0, -1))
            if obs.ver_direcao("Sul") == "Vazio":   possiveis.append((0, 1))
            if obs.ver_direcao("Este") == "Vazio":  possiveis.append((1, 0))
            if obs.ver_direcao("Oeste") == "Vazio": possiveis.append((-1, 0))

            if possiveis:
                dx, dy = random.choice(possiveis)
                return Accao.mover(dx, dy)

            return Accao(TipoAccao.FAZER_NADA)

    def selecionar_acao_ficheiro(self, estado: Tuple[int, int]) -> Accao:
        if not hasattr(self, 'q_table'):
            return None
        acoes_possiveis = [
            (0, -1, "Norte"), (0, 1, "Sul"), (1, 0, "Este"), (-1, 0, "Oeste")
        ]

        melhor_q = -float('inf')
        melhor_acao = None

        encontrou_alguma = False

        for dx, dy, nome in acoes_possiveis:
            if (estado, nome) in self.q_table:
                encontrou_alguma = True
                q_val = self.q_table[(estado, nome)]
                if q_val > melhor_q:
                    melhor_q = q_val
                    melhor_acao = (dx, dy)

        if encontrou_alguma and melhor_acao:
            return Accao.mover(melhor_acao[0], melhor_acao[1])
        return None