from Politica import Politica
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

        return (0, 0)