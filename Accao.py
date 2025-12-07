from enum import Enum

class TipoAccao(Enum):
    MOVER = "MOVER"         # Usada no Farol e Labirinto
    COMUNICAR = "COMUNICAR" # Usada no Labirinto
    FAZER_NADA = "NADA"     # Usada para esperar

class Accao:
    def __init__(self, tipo: TipoAccao, parametros: dict = None):
        self.tipo = tipo
        self.parametros = parametros if parametros is not None else {}

    @staticmethod
    def mover(dx: int, dy: int):
        return Accao(TipoAccao.MOVER, {'dx': dx, 'dy': dy})

    @staticmethod
    def comunicar(mensagem: str):
        return Accao(TipoAccao.COMUNICAR, {'msg': mensagem})