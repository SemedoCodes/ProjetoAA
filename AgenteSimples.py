from Agente import Agente
from Acao import Acao, TipoAcao
from Posicao import Posicao

def __init_ (self, passos_max, posicao: Posicao, conhecimento: dict):
    self.passos_max = passos_max
    self.posicao = posicao
    conhecimento = []

def cria(nome_do_ficheiro_parametros: str):
    pass
    
def observacao(self, obs):
    self.conhecimento.append(obs)

def age(self):
    return self.politica.selecionar_acao(self.obs)


