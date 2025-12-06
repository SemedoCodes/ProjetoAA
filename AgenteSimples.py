import json
from Agente import Agente
from Posicao import Posicao
from Politica import Politica


class AgenteSimples(Agente):
    def __init__(self, passos_max: int, posicao: Posicao, politica: Politica):
        self.passos_max = passos_max
        self.posicao = posicao
        self.politica = politica
        self.conhecimento = []      # agora é atributo da instância
        self.ultima_obs = None

    def cria(self, nome_do_ficheiro_parametros: str):
        with open(nome_do_ficheiro_parametros, "r") as f:
            params = json.load(f)

        self.passos_max = params.get("passos_max", self.passos_max)
        x, y = params.get("posicao_inicial", [self.posicao.x, self.posicao.y])
        self.posicao = Posicao(x, y)

        
      #  ficheiro_politica = params.get("ficheiro_politica")
      #  if ficheiro_politica and hasattr(self.politica, "carregar_politica"):
      #      self.politica.carregar_politica(ficheiro_politica)

    def observacao(self, obs):
        self.ultima_obs = obs          
        self.conhecimento.append(obs)

    def age(self):
       
        if self.ultima_obs is None:
            return None                  # ou uma ação neutra
        return self.politica.selecionar_acao(self.ultima_obs)
