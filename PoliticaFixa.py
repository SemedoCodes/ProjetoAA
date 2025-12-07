from Politica import Politica
from Observacao import Observacao
from Accao import Acao, TipoAccao
from typing import Dict, Any
import random

class PoliticaFixa(Politica):
    """
    Política de agente com regras fixas/determinísticas.
    Usado para o Modo de Teste ou agentes que não aprendem.
    """

    def __init__(self):
        self.regras_fixas = {}
        self.nome = "Política Fixa"

    def carregar_politica(self, ficheiro: str):
        """
        Carrega as regras a partir de um ficheiro.
        """
        self.regras_fixas = {

        }

    def selecionar_acao(self, obs) -> Acao:
        """
        Consulta as regras com base no que o agente viu.
        """
        if obs.tem_vetor():
            dx_total, dy_total = obs.vetor_farol

            # se ambos forem 0, estamos em cima do farol
            if dx_total == 0 and dy_total == 0:
                return Acao(TipoAccao.FAZER_NADA)

            # se a distância horizontal for maior ou igual à vertical -> move em X
            if abs(dx_total) >= abs(dy_total):
                if dx_total > 0:
                    return Acao.mover(1, 0)  # Mover Este
                else:
                    return Acao.mover(-1, 0)  # Mover Oeste

            # mover em Y
            else:
                if dy_total > 0:
                    return Acao.mover(0, 1)  # Mover Sul
                else:
                    return Acao.mover(0, -1)  # Mover Norte
        else:
            possiveis = []
            if obs.ver_direcao("Norte") == "Saida": return Acao.mover(0, -1)
            if obs.ver_direcao("Sul") == "Saida":   return Acao.mover(0, 1)
            if obs.ver_direcao("Este") == "Saida":  return Acao.mover(1, 0)
            if obs.ver_direcao("Oeste") == "Saida": return Acao.mover(-1, 0)

            if obs.ver_direcao("Norte") == "Vazio": possiveis.append((0, -1))
            if obs.ver_direcao("Sul") == "Vazio":   possiveis.append((0, 1))
            if obs.ver_direcao("Este") == "Vazio":  possiveis.append((1, 0))
            if obs.ver_direcao("Oeste") == "Vazio": possiveis.append((-1, 0))

            if possiveis:
                dx, dy = random.choice(possiveis)
                return Acao.mover(dx, dy)

            return Acao(TipoAccao.FAZER_NADA)