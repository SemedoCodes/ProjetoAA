from Politica import Politica

class PoliticaAprendizagem(Politica):

    def __init__(self):
        self.regras_fixas = {}
        self.nome = "Política Aprendizagem"