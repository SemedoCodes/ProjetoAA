from typing import List, Dict, Optional, Tuple
from Posicao import Posicao

class Observacao:
    """
    Pacote de dados que o Ambiente entrega ao Agente.
    Contém apenas o que o agente consegue ver num dado momento
    """
    def __init__(self, posicao_agente: Posicao,
                 vetor_farol: Optional[Tuple[int, int]] = None,
                 vizinhanca: Optional[Dict[str, str]] = None,
                 posicoes_risco: Optional[List[Posicao]] = None):

        self.posicao = posicao_agente
        self.vetor_farol = vetor_farol # Vetor (dx, dy) para o Farol
        self.vizinhanca = vizinhanca if vizinhanca else {} # Visão local para o Labirinto
        self.posicoes_risco = posicoes_risco if posicoes_risco else []

    def tem_vetor(self) -> bool:
        return self.vetor_farol is not None

    def ver_direcao(self, direcao: str) -> str:
        return self.vizinhanca.get(direcao, "Desconhecido")