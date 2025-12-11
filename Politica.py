from abc import ABC, abstractmethod
from typing import Dict, Any

class Politica(ABC):
    @abstractmethod
    def selecionar_acao(self, observacao: 'Observacao') -> 'Accao':
        """
        Recebe a observação do Ambiente e
        devolve a ação a ser executada.
        """
        pass

   
    def carregar_politica(self, ficheiro: str):
        # carrega a Q-Table de um ficheiro txt

        self.q_table = {}
        with open(ficheiro, "r") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                x_str, y_str, acao, q_str = linha.split(",")
                estado = (int(x_str), int(y_str))
                q = float(q_str)
                self.q_table[(estado, acao)] = q   