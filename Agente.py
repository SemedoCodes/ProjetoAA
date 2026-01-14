from abc import ABC, abstractmethod
from Elemento import Elemento
from Posicao import Posicao
from Observacao import Observacao
import threading

class Agente(Elemento, threading.Thread, ABC):
    """
    Classe base abstrata para um Agente Autónomo.
    """
    def __init__ (self, id_agente: int, posicao: Posicao):
        super().__init__(f"Agente {id_agente}", posicao, "A", True)
        threading.Thread.__init__(self)

        self.id = id_agente
        self.recompensa_acumulada = 0.0
        self.sensores = []
        self.politica = None
        self.ultima_observacao = None
        self.mensagens_recebidas = []

        # Controlo da thread
        self.ativo = True
        self.ambiente_ref = None
        self.barreira = None

    def definir_politica(self, politica):
        self.politica = politica

    def instala (self, sensor):
        self.sensores.append(sensor)

    # Recebe mensagem de outro agente
    def comunica(self, mensagem: str, de_agente: 'Agente'):
        self.mensagens_recebidas.append(mensagem)

    def set_sincronizacao(self, ambiente, barreira):
        self.ambiente_ref = ambiente
        self.barreira = barreira

    # Define a lógica de decisão
    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def configura_ambiente(self, id_agente: int, posicao: Posicao):
        pass

    # Ciclo de vida da Thread do Agente
    def run(self):
       while self.ativo:
            try:
                if not self.ambiente_ref: continue

                # Perceber
                obs = self.ambiente_ref.observacaoPara(self)
                self.ultima_observacao = obs

                # Decidir
                acao = self.age()

                # Agir
                recompensa = self.ambiente_ref.agir(acao, self)

                # Aprender
                obs_nova = self.ambiente_ref.observacaoPara(self)

                r_total = recompensa
                if hasattr(self, 'processar_recompensa'):
                    r_total = self.processar_recompensa(recompensa, obs_nova)

                if self.politica and hasattr(self.politica, 'aprende'):
                    self.politica.aprende(obs, acao, r_total, obs_nova)

                self.recompensa_acumulada += r_total

                # Sincronizar
                if self.barreira:
                    self.barreira.wait()

            except threading.BrokenBarrierError:
                break

    def parar(self):
        self.ativo = False