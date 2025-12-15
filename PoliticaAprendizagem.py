import random
import json
from Politica import Politica
from Accao import Accao, TipoAccao
from Observacao import Observacao


class PoliticaAprendizagem(Politica):


    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.nome = "PolíticaAprendizagem"

        self.alpha = alpha # taxa de aprendizagem: define a velocidade com que o
        # agente substitui o conhecimento antigo
        self.gamma = gamma # fator de desconto: define o peso das recompensas
        # futuras na decisão atual
        self.epsilon = epsilon # taxa de exploração: define a problabilidade de
        # o agente ignorar o que sabe e tentar algo aleatório para
        # descobrir novos caminhos

        self.acoes_possiveis = [
            (0, -1, "Norte"),
            (0, 1, "Sul"),
            (1, 0, "Este"),
            (-1, 0, "Oeste")
        ]


    def _get_estado(self, obs: Observacao):
        return (obs.posicao.x, obs.posicao.y)


    def _get_q(self, estado, acao_str):
        return self.q_table.get((estado, acao_str), 0.0)


    def selecionar_acao(self, obs: Observacao) -> Accao:
        # 1) Fundir Q-Tables recebidas de outros agentes (apenas QTABLE)
        if hasattr(obs, 'mensagens') and obs.mensagens:
            for msg in obs.mensagens:
                if isinstance(msg, dict) and msg.get("tipo") == "QTABLE":
                    self.fundir_q_table(msg)

        estado = self._get_estado(obs)
        
        # explorar (Escolher aleatoriamente)
        if random.random() < self.epsilon:
            dx, dy, _ = random.choice(self.acoes_possiveis)
            return Accao.mover(dx, dy)

        # aproveitar (Escolher a melhor ação da Q-Table)
        melhor_q = -float('inf') # ajuda a guardar a melhor acao possivel
        melhores_acoes = []

        for dx, dy, nome in self.acoes_possiveis:
            q_val = self._get_q(estado, nome)

            if q_val > melhor_q:
                melhor_q = q_val
                melhores_acoes = [(dx, dy)]
            elif q_val == melhor_q:
                melhores_acoes.append((dx, dy))

        # desempate aleatório entre as melhores
        dx, dy = random.choice(melhores_acoes)
        return Accao.mover(dx, dy)


    def aprende(self, obs_anterior: Observacao, acao: Accao, recompensa: float, obs_nova: Observacao):
        """
        equação de Bellman.
        Q(s,a) = Q(s,a) + alpha * [r + gamma * max(Q(s', a')) - Q(s,a)]
        """
        # 1. identificar Estado (s) e Ação (a)
        estado_ant = self._get_estado(obs_anterior)

        dx = acao.parametros.get('dx', 0)
        dy = acao.parametros.get('dy', 0)
        acao_str = "Nulo"
        if dx == 0 and dy == -1:
            acao_str = "Norte"
        elif dx == 0 and dy == 1:
            acao_str = "Sul"
        elif dx == 1 and dy == 0:
            acao_str = "Este"
        elif dx == -1 and dy == 0:
            acao_str = "Oeste"

        if acao_str == "Nulo":
            return

        # 2. identificar novo Estado (s')
        estado_novo = self._get_estado(obs_nova)

        # 3. calcular o max Q(s', a') (melhor valor futuro possível)
        max_q_futuro = -float('inf')
        for _, _, nome_prox in self.acoes_possiveis:
            q_val = self._get_q(estado_novo, nome_prox)
            if q_val > max_q_futuro:
                max_q_futuro = q_val

        # e não houver valores na tabela para o prox estado, assume 0
        if max_q_futuro == -float('inf'): max_q_futuro = 0.0

        # 4. atualizar Q(s, a)
        q_atual = self._get_q(estado_ant, acao_str)

        # fórmula do Q-Learning
        novo_q = q_atual + self.alpha * (recompensa + (self.gamma * max_q_futuro) - q_atual)

        self.q_table[(estado_ant, acao_str)] = novo_q


    def guardar_politica(self, ficheiro: str):
       #Guarda a Q-Table num ficheiro txt
       with open (ficheiro, "w") as f:
           for (estado, acao), q in self.q_table.items():
               x, y = estado
               f.write(f"{x},{y},{acao},{q}\n")


    def construir_mensagem_qtable(self, limite: int = 200):
        #Devolve um dict com parte da Q-Table.
        #limite: nº máximo de entradas incluídas.
        itens = list(self.q_table.items())
        # opcional: ordena pelas ações mais valiosas
        itens = sorted(itens, key=lambda kv: kv[1], reverse=True)[:limite]

        dados = []
        for (estado, acao_str), q in itens:
            x, y = estado
            dados.append({"x": x, "y": y, "acao": acao_str, "q": q})

        return {"tipo": "QTABLE", "dados": dados}
    
    def fundir_q_table(self, msg_qtable: dict, peso_externa: float = 0.5):
        """
        Atualiza Q-Table local com valores recebidos.
        msg_qtable: dict {"tipo": "QTABLE", "dados": [ {x,y,acao,q}, ... ]}
        peso_externa: peso dado ao conhecimento externo.
        """
        if not msg_qtable or msg_qtable.get("tipo") != "QTABLE":
            return

        for item in msg_qtable.get("dados", []):
            try:
                x = int(item["x"])
                y = int(item["y"])
                acao_str = str(item["acao"])
                q_ext = float(item["q"])
            except (KeyError, ValueError, TypeError):
                continue

            estado = (x, y)
            q_local = self._get_q(estado, acao_str)
            if q_ext > q_local:
                self.q_table[(estado, acao_str)] = q_ext
