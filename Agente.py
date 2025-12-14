from abc import ABC, abstractmethod
from Elemento import Elemento
from Posicao import Posicao
from Observacao import Observacao
import threading

class Agente(Elemento, threading.Thread, ABC):

    def __init__ (self, id_agente: int, posicao: Posicao):
        super().__init__(f"Agente {id_agente}", posicao, "A", True)
        threading.Thread.__init__(self)
        self.id = id_agente
        self.recompensa_acumulada = 0.0
        self.sensores = []  # lista de sensores
        self.politica = None
        self.ultima_observacao = None
        self.mensagens_recebidas = []

        # controlo da thread
        self.ativo = True
        self.ambiente_ref = None # para o agente agir sozinho
        self.barreira = None # para sincronizar com o motor

    def definir_politica(self, politica):
        self.politica = politica

    def cria(self, nome_do_ficheiro: str):
        pass

    def observacao(self, obs: Observacao):
        self.ultima_observacao = obs

    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def configura_ambiente(self, id_agente: int, posicao: Posicao):
        pass

    def avaliacaoEstadoAtual(self, recompensa: float):
        self.recompensa_acumulada += recompensa

    def instala (self, sensor):
        self.sensores.append(sensor)

    def comunica(self, mensagem: str, de_agente: 'Agente'):
        self.mensagens_recebidas.append(mensagem)
        print(f"[{self.nome}] Recebi: {mensagem}")

    def set_sincronizacao(self, ambiente, barreira):
        self.ambiente_ref = ambiente
        self.barreira = barreira

    def run(self):
       while self.ativo:
            try:
                # 1. Perceber e Pensar
                obs = self.ambiente_ref.observacaoPara(self)
                self.observacao(obs)
                acao = self.age()

                # 2. Agir (Executa diretamente no ambiente)
                recompensa = self.ambiente_ref.agir(acao, self)

                # 3. Aprender
                obs_nova = self.ambiente_ref.observacaoPara(self)

                # Soma recompensas (Intrínseca + Extrínseca)
                r_total = recompensa
                if hasattr(self, 'processar_recompensa'):
                    r_total = self.processar_recompensa(recompensa, obs_nova)

                if self.politica and hasattr(self.politica, 'aprende'):
                    self.politica.aprende(obs, acao, r_total, obs_nova)

                self.avaliacaoEstadoAtual(r_total)

                # 4. ESPERAR PELOS OUTROS (Sincronização)
                # O agente fica aqui parado até todos os outros agentes
                # e o Motor chegarem a este ponto.
                if self.barreira:
                    self.barreira.wait()

            except threading.BrokenBarrierError:
                break

    def parar(self):
        self.ativo = False