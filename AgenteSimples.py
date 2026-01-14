from typing import Any, Dict, Set, List, Tuple
from Agente import Agente
from Accao import Accao, TipoAccao
from PoliticaAprendizagem import PoliticaAprendizagem
from PoliticaFixa import PoliticaFixa
from Posicao import Posicao
from SensorBussola import SensorBussola
from SensorVisao import SensorVisao
from Observacao import Observacao

class AgenteSimples(Agente):
    """
    Agente que implementa a lógica de recompensas e comunicação
    """

    def __init__(self, id_agente: int, posicao: Posicao):
        super().__init__(id_agente, posicao)
        self.celulas_visitadas_proprias: Set[Tuple[int, int]] = set()
        self.passos_sem_comunicar = 0
        self.passos_entre_comunicacoes = 20
        self.tipo_problema = " "

    @classmethod
    def cria(cls, nome_do_ficheiro_parametros: str) -> 'AgenteSimples':
        parametros: Dict[str, Any] = {}
        try:
            with open(nome_do_ficheiro_parametros, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith('#'): continue
                    chave, valor = linha.split('=', 1)
                    parametros[chave.strip()] = valor.strip()
        except FileNotFoundError:
            print(f"ERRO (Agente): Ficheiro de parâmetros '{nome_do_ficheiro_parametros}' não encontrado.")

        novo_agente = cls(id_agente=0, posicao=Posicao(0, 0))

        # Configurar política
        politica_nome = parametros.get('tipo_politica', 'PoliticaFixa')
        if politica_nome == 'PoliticaFixa':
            politica = PoliticaFixa()
            if 'ficheiro_teste' in parametros and parametros['ficheiro_teste']:
                politica.carregar_politica(parametros['ficheiro_teste'])
            novo_agente.definir_politica(politica)
        else:
            novo_agente.definir_politica(PoliticaAprendizagem())

        # Configurar Sensores
        novo_agente.tipo_problema = parametros.get('tipo_problema', 'Farol')
        if novo_agente.tipo_problema == 'Farol':
            novo_agente.instala(SensorBussola())
        else:
            novo_agente.instala(SensorVisao())

        return novo_agente

    def configura_ambiente(self, id_agente: int, posicao_inicial: Posicao):
        self.id = id_agente
        self.nome = f"Agente {id_agente}"
        self.posicao = posicao_inicial

    # Recebe Q-Table de outros agentes e funde com a sua
    def comunica(self, mensagem, de_agente):
        if self.politica and hasattr(self.politica, 'fundir_q_table'):
            self.politica.fundir_q_table(mensagem)

    def age(self) -> Accao:
        if not self.ultima_observacao or not self.politica:
            return Accao(TipoAccao.FAZER_NADA)
        
        # Lógica de comunicação
        self.passos_sem_comunicar += 1
        if self.passos_sem_comunicar >= self.passos_entre_comunicacoes:
            if hasattr(self.politica, 'construir_mensagem_qtable'):
                msg_qtable = self.politica.construir_mensagem_qtable(limite=50)
                self.passos_sem_comunicar = 0  # reset
                return Accao.comunicar(msg_qtable)

        return self.politica.selecionar_acao(self.ultima_observacao)

    def processar_recompensa(self, recompensa_extrinseca: float, obs_nova: Observacao) -> float:
        pos_atual = (self.posicao.x, self.posicao.y)

        if self.tipo_problema == "Labirinto":
            if pos_atual not in self.celulas_visitadas_proprias:
                self.celulas_visitadas_proprias.add(pos_atual)

        return recompensa_extrinseca

    def fim_do_episodio(self):
        if self.politica and hasattr(self.politica, 'atualizar_epsilon_fim_episodio'):
            self.politica.atualizar_epsilon_fim_episodio()