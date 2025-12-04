from Sensor import Sensor
from Farol import Farol

class SensorBussola(Sensor):
    def __init__(self):
        super().__init__("Bússola")

    def ler(self, ambiente, agente):
        pos_farol = None
        for elem in ambiente.elementos:
            if isinstance(elem, Farol):
                pos_farol = elem.posicao
                break

        if pos_farol:
            return (pos_farol.x - agente.posicao.x, pos_farol.y - agente.posicao.y)
        return None

