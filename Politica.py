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

    @abstractmethod
    def carregar_politica(self, ficheiro: str):
        """
        Carrega a política de um ficheiro (regras ou Q-Table).
        """
        pass

