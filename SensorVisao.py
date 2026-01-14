from Sensor import Sensor
from Posicao import Posicao
from Saida import Saida
from Parede import Parede
from Obstaculo import Obstaculo

class SensorVisao(Sensor):
    """
    Verifica 4 células (N, S, E ,O).
    """
    def __init__(self):
        super().__init__("Visão 3x3")

    def ler(self, ambiente, agente):
        visao = {}
        direcoes = {
            "Norte": (0, -1),
            "Sul": (0, 1),
            "Oeste": (-1, 0),
            "Este": (1, 0)
        }

        for nome_dir, (dx, dy) in direcoes.items():
            pos_ver = Posicao(agente.posicao.x + dx, agente.posicao.y + dy)

            # Verifica limites
            if not (0 <= pos_ver.x < ambiente.largura and 0 <= pos_ver.y < ambiente.altura):
                visao[nome_dir] = "Parede"
                continue

            # Verifica objetos
            objs = ambiente.todos_elementos_posicao(pos_ver)
            if not objs:
                visao[nome_dir] = "Vazio"
            else:
                primeiro_obj = objs[0]

                if isinstance(primeiro_obj, Saida): visao[nome_dir] = "Saida"
                elif isinstance(primeiro_obj, Parede) or isinstance(primeiro_obj, Obstaculo): visao[nome_dir] = "Parede"
                else: visao[nome_dir] = "Vazio"

        return visao