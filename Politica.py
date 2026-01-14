from abc import ABC, abstractmethod

class Politica(ABC):
    """
    Interface para estratégias de decisão.
    """
    @abstractmethod
    def selecionar_acao(self, observacao: 'Observacao') -> 'Accao':
        pass

    # Carrega Q-Tables
    def carregar_politica(self, ficheiro: str):
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