from Sensor import Sensor
from Posicao import Posicao
from Saida import Saida
from Parede import Parede
from Obstaculo import Obstaculo

class SensorVisao(Sensor):
    def __init__(self):
        super().__init__("Visão 3x3")

    def ler(self, ambiente, agente):
        """
        Retorna um dicionário: {'Norte': 'Parede', 'Sul': 'Vazio', ...}
        """
        visao = {}
        direcoes = {
            "Norte": (0, -1),
            "Sul": (0, 1),
            "Oeste": (-1, 0),
            "Este": (1, 0)
        }

        for nome_dir, (dx, dy) in direcoes.items():
            x_ver = agente.posicao.x + dx
            y_ver = agente.posicao.y + dy
            pos_ver = Posicao(x_ver, y_ver)

            if not (0 <= x_ver < ambiente.largura and 0 <= y_ver < ambiente.altura):
                visao[nome_dir] = "Parede"
                continue

            objs = ambiente.todos_elementos_posicao(pos_ver)

            if not objs:
                visao[nome_dir] = "Vazio"
            else:
                primeiro_obj = objs[0]

                if isinstance(primeiro_obj, Saida):
                    visao[nome_dir] = "Saida"
                elif isinstance(primeiro_obj, Parede) or isinstance(primeiro_obj, Obstaculo):
                    visao[nome_dir] = "Parede"
                else:
                    visao[nome_dir] = "Vazio"
        return visao