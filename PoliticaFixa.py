from Politica import Politica
from typing import Dict, Any

class PoliticaFixa(Politica):
    """
    Política de agente com regras fixas/determinísticas.
    Ideal para o Modo de Teste ou agentes que não aprendem.
    """

    def __init__(self):
        # Onde as regras (a política) serão armazenadas.
        self.regras_determinísticas = {}
        self.nome = "Política Fixa"

    def carregar_politica(self, ficheiro: str):
        """
        Carrega as regras a partir de um ficheiro.
        """
        self.regras_determinísticas = {

        }

    def selecionar_acao(self, observacao: Dict[str, Any]) -> Any:
        """
        Implementa a lógica de decisão: consulta as regras fixas
        com base no que é visto pelo agente.
        """

        return (0, 0)