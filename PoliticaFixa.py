from Politica import Politica
from Observacao import Observacao
from Acao import Acao, TipoAcao
from typing import Dict, Any

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
            dx_total, dy_total = obs.vetor_alvo

            # se ambos forem 0, estamos em cima do farol
            if dx_total == 0 and dy_total == 0:
                return Acao(TipoAcao.FAZER_NADA)

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

            return Acao(TipoAcao.FAZER_NADA)
        return (0, 0)