from Politica import Politica
from Acao import Acao, TipoAcao

class PoliticaAprendizagem(Politica):

    def __init__(self):
        self.regras_fixas = {}
        self.nome = "Política Aprendizagem"

    def selecionar_acao(self, obs):
        return Acao(TipoAcao.FAZER_NADA)  # Placeholder

    def carregar_politica(self, ficheiro):
        pass