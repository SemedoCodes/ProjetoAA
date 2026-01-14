from Politica import Politica
from Accao import Accao, TipoAccao
from typing import Tuple
import random

class PoliticaFixa(Politica):
    """
    Política determinística para testes.
    """

    def __init__(self):
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

        # Tenta ler do ficheiro
        acao_teste = self.selecionar_acao_ficheiro(estado_atual)
        if acao_teste: return acao_teste

        # Lógica do Farol
        if obs.tem_vetor():
            # Deteta colisão
            colisao = (self.ultima_posicao is not None and self.ultima_posicao == estado_atual)
            self.ultima_posicao = estado_atual

            # Se bateu, faz movimenro aleatório
            if colisao:
                opcoes = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1)]
                dx, dy = random.choice(opcoes)
                return Accao.mover(dx, dy)

            dx_total, dy_total = obs.vetor_farol

            # Atingiu o objetivo
            if dx_total == 0 and dy_total == 0:
                return Accao(TipoAccao.FAZER_NADA)

            # Reduzir a maior distância
            if abs(dx_total) >= abs(dy_total):
                return Accao.mover(1 if dx_total > 0 else -1, 0)
            else:
                return Accao.mover(0, 1 if dy_total > 0 else -1)

        # Lógica do Labirinto
        else:
            possiveis = []
            mapa = [("Norte", 0, -1), ("Sul", 0, 1), ("Este", 1, 0), ("Oeste", -1, 0)]

            # Pioridade -> Saída
            for d_nome, dx, dy in mapa:
                if obs.ver_direcao(d_nome) == "Saida": return Accao.mover(dx, dy)

            # Movimento Aleatório nas células vazias
            for d_nome, dx, dy in mapa:
                if obs.ver_direcao(d_nome) == "Vazio": possiveis.append((dx, dy))

            if possiveis:
                dx, dy = random.choice(possiveis)
                return Accao.mover(dx, dy)

            return Accao(TipoAccao.FAZER_NADA)

    # Usa Q-Table pré-carregada se existir
    def selecionar_acao_ficheiro(self, estado: Tuple[int, int]) -> Accao:
        if not hasattr(self, 'q_table'): return None

        acoes_possiveis = [(0, -1, "Norte"), (0, 1, "Sul"), (1, 0, "Este"), (-1, 0, "Oeste")]
        melhor_q = -float('inf')
        melhor_acao = None

        for dx, dy, nome in acoes_possiveis:
            val = self.q_table.get((estado, nome))
            if val is not None and val > melhor_q:
                melhor_q = val
                melhor_acao = (dx, dy)

        if melhor_acao:
            return Accao.mover(*melhor_acao)
        return None