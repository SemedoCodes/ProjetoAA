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
    celulas_visitadas_global: Set[Tuple[int, int]] = set() # memoria partilhada pelos agentes

    def __init__(self, id_agente: int, posicao: Posicao):
        super().__init__(id_agente, posicao)

        # recompensas intrínsecas
        self.celulas_visitadas_proprias: Set[Tuple[int, int]] = set()
        self.historico_recente: List[Tuple[int, int]] = []  # Para detetar loops
        self.distancia_anterior_farol = float('inf')

        self.tipo_problema = " "

    @classmethod
    def cria(cls, nome_do_ficheiro_parametros: str) -> 'AgenteSimples':

        # ler os parametros
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

        politica_nome = parametros.get('tipo_politica', 'PoliticaFixa')

        if politica_nome == 'PoliticaFixa':
            politica = PoliticaFixa()
            ficheiro_teste = parametros.get('ficheiro_teste')
            if ficheiro_teste:
                politica.carregar_politica(ficheiro_teste)
            novo_agente.definir_politica(politica)
        elif politica_nome == 'PoliticaAprendizagem':
            novo_agente.definir_politica(PoliticaAprendizagem())
        else:
            print(f"Aviso (Agente): Política '{politica_nome}' desconhecida. Usando PoliticaFixa.")
            novo_agente.definir_politica(PoliticaFixa())

        novo_agente.tipo_problema = parametros.get('tipo_problema', 'Farol')

        if novo_agente.tipo_problema == 'Farol':
            novo_agente.instala(SensorBussola())
        elif novo_agente.tipo_problema == 'Labirinto':
            novo_agente.instala(SensorVisao())
        else:
            novo_agente.instala(SensorVisao())
            novo_agente.instala(SensorBussola())

        return novo_agente

    def configura_ambiente(self, id_agente: int, posicao_inicial: Posicao):
        self.id = id_agente
        self.posicao = posicao_inicial

    def age(self) -> Accao:
        if self.ultima_observacao is None or self.politica is None:
            return Accao(TipoAccao.FAZER_NADA)
        acao = self.politica.selecionar_acao(self.ultima_observacao)

        return acao

    def processar_recompensa(self, recompensa_extrinseca: float, obs_nova: Observacao) -> float:
        recompensa_intrinseca = 0.0
        pos_atual = (self.posicao.x, self.posicao.y)

        # farol
        if self.tipo_problema == "Farol" and obs_nova.tem_vetor():
            dx, dy = obs_nova.vetor_farol
            distancia = abs(dx) + abs(dy)

            if distancia < self.distancia_anterior_farol:
                recompensa_intrinseca += 0.5 # recompensa por aproximar

            self.distancia_anterior_farol = distancia

            if len(self.historico_recente) >= 2 and pos_atual == self.historico_recente[-2]:
                recompensa_intrinseca -= 0.2 # penalidade por repetir os mesmos passos

        # labirinto
        elif self.tipo_problema == "Labirinto":
            if pos_atual not in self.celulas_visitadas_proprias:
                recompensa_intrinseca += 1.0 # recompensa por visitar uma celula nova
                self.celulas_visitadas_proprias.add(pos_atual)

            paredes_a_volta = 0
            for direcao in ["Norte", "Sul", "Este", "Oeste"]:
                obs_ver = obs_nova.ver_direcao(direcao)

                if obs_ver == "Parede" or obs_ver == "Obstaculo":
                    paredes_a_volta += 1

            if paredes_a_volta >= 3:
                recompensa_intrinseca -= 0.2 # recompensa por dead-end


        # atualiza histórico
        self.historico_recente.append(pos_atual)
        if len(self.historico_recente) > 10: self.historico_recente.pop(0)

        return recompensa_extrinseca + recompensa_intrinseca