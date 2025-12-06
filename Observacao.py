from typing import List, Dict, Optional, Tuple
from Posicao import Posicao

class Observacao:
    # criado pelo ambiente e usado pela política do agente
    def __init__(self, posicao_agente: Posicao,
                 vetor_farol: Optional[Tuple[int, int]] = None,
                 vizinhanca: Optional[Dict[str, str]] = None,
                 posicoes_risco: Optional[List[Posicao]] = None):
        self.posicao = posicao_agente
        self.vetor_farol = vetor_farol # vetor (dx, dy) a indicar a direção do farol
        self.vizinhanca = vizinhanca if vizinhanca else {}
        self.posicoes_risco = posicoes_risco if posicoes_risco else []

    def tem_vetor(self) -> bool:
        return self.vetor_farol is not None

    def ver_direcao(self, direcao: str) -> str:
        return self.vizinhanca.get(direcao, "Desconhecido")

    def posicao_e_risco(self, posicao: Posicao) -> bool:
        return posicao in self.posicoes_risco