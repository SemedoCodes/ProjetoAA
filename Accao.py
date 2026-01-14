from enum import Enum

class TipoAccao(Enum):
    MOVER = "MOVER"         # Deslocamento
    COMUNICAR = "COMUNICAR" # Troca de mensagens (Q-Table)
    FAZER_NADA = "NADA"     # Espera

class Accao:
    """
    Encapsula uma decisão do agente.
    Pode conter parâmetros como 'dx', 'dy' ou 'msg'.
    """
    def __init__(self, tipo: TipoAccao, parametros: dict = None):
        self.tipo = tipo
        self.parametros = parametros if parametros is not None else {}

    @staticmethod
    def mover(dx: int, dy: int):
        return Accao(TipoAccao.MOVER, {'dx': dx, 'dy': dy})

    @staticmethod
    def comunicar(mensagem: str):
        return Accao(TipoAccao.COMUNICAR, {'msg': mensagem})