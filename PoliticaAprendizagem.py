import random
from Politica import Politica
from Accao import Accao
from Observacao import Observacao

class PoliticaAprendizagem(Politica):
    """
    Implementa o algoritmo Q-Learning.
    Implementa fusão de conhecimento entre agentes.
    """

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.q_table = {}
        self.nome = "PolíticaAprendizagem"

        self.alpha = alpha # Taxa de Aprendizagem
        self.gamma = gamma # Fator de desconto

        self.epsilon = epsilon # Taxa de exploração
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay # Fator de decaimento

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
        # Processar conhecimento recebido
        if hasattr(obs, 'mensagens') and obs.mensagens:
            for msg in obs.mensagens:
                if isinstance(msg, dict) and msg.get("tipo") == "QTABLE":
                    self.fundir_q_table(msg)

        estado = self._get_estado(obs)
        
        # Exploração
        if random.random() < self.epsilon:
            dx, dy, _ = random.choice(self.acoes_possiveis)
            return Accao.mover(dx, dy)

        # Escolher a melhor ação conhecida
        melhor_q = -float('inf')
        melhores_acoes = []

        for dx, dy, nome in self.acoes_possiveis:
            q_val = self._get_q(estado, nome)
            if q_val > melhor_q:
                melhor_q = q_val
                melhores_acoes = [(dx, dy)]
            elif q_val == melhor_q:
                melhores_acoes.append((dx, dy))

        dx, dy = random.choice(melhores_acoes)
        return Accao.mover(dx, dy)

    # Atualiza a Q-Table
    def aprende(self, obs_anterior: Observacao, acao: Accao, recompensa: float, obs_nova: Observacao):
        estado_ant = self._get_estado(obs_anterior)
        estado_novo = self._get_estado(obs_nova)

        # Mapear ação para string
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

        # Calcular o Max Q oara o estado seguinte
        max_q_futuro = -float('inf')
        for _, _, nome_prox in self.acoes_possiveis:
            q_val = self._get_q(estado_novo, nome_prox)
            if q_val > max_q_futuro:
                max_q_futuro = q_val
        if max_q_futuro == -float('inf'): max_q_futuro = 0.0

        # Atualiza Q-Value
        q_atual = self._get_q(estado_ant, acao_str)
        novo_q = q_atual + self.alpha * (recompensa + (self.gamma * max_q_futuro) - q_atual)

        self.q_table[(estado_ant, acao_str)] = novo_q

    # Reduz a taxa de exploração no final de cada episódio
    def atualizar_epsilon_fim_episodio(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def guardar_politica(self, ficheiro: str):
       with open (ficheiro, "w") as f:
           for (estado, acao), q in self.q_table.items():
               x, y = estado
               f.write(f"{x},{y},{acao},{q}\n")


    def construir_mensagem_qtable(self, limite: int = 200):
        # Prepara uma lista com os melhores dados da Q-Table para partilhar
        itens = list(self.q_table.items())
        itens = sorted(itens, key=lambda kv: kv[1], reverse=True)[:limite]
        dados = []
        for (estado, acao_str), q in itens:
            x, y = estado
            dados.append({"x": x, "y": y, "acao": acao_str, "q": q})
        return {"tipo": "QTABLE", "dados": dados}
    
    def fundir_q_table(self, msg_qtable: dict, peso_externa: float = 0.5):
        # Integra conhecimento externo se for melhor que o local
        if not msg_qtable or msg_qtable.get("tipo") != "QTABLE": return

        for item in msg_qtable.get("dados", []):
            try:
                estado = (int(item["x"]), int(item["y"]))
                acao = str(item["acao"])
                q_ext = float(item["q"])

                if q_ext > self._get_q(estado, acao):
                    self.q_table[(estado, acao)] = q_ext
            except:
                continue