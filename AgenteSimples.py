from typing import Any, Dict

from Agente import Agente
from Accao import Acao, TipoAccao
from PoliticaAprendizagem import PoliticaAprendizagem
from PoliticaFixa import PoliticaFixa
from Posicao import Posicao
from SensorBussola import SensorBussola
from SensorVisao import SensorVisao


class AgenteSimples(Agente):
    def __init__(self, id_agente: int, posicao: Posicao):
        super().__init__(id_agente, posicao)

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
            novo_agente.definir_politica(PoliticaFixa())
        elif politica_nome == 'PoliticaAprendizagem':
            novo_agente.definir_politica(PoliticaAprendizagem())
        else:
            print(f"Aviso (Agente): Política '{politica_nome}' desconhecida. Usando PoliticaFixa.")
            novo_agente.definir_politica(PoliticaFixa())

        tipo_problema = parametros.get('tipo_problema', 'Farol')

        if tipo_problema == 'Farol':
            novo_agente.instala(SensorBussola())
        elif tipo_problema == 'Labirinto':
            novo_agente.instala(SensorVisao())
        else:
            novo_agente.instala(SensorVisao())
            novo_agente.instala(SensorBussola())

        return novo_agente

    def configura_ambiente(self, id_agente: int, posicao_inicial: Posicao):
        self.id = id_agente
        self.posicao = posicao_inicial

    def age(self) -> Acao:
        if self.ultima_observacao is None or self.politica is None:
            return Acao(TipoAccao.FAZER_NADA)
        acao = self.politica.selecionar_acao(self.ultima_observacao)

        return acao

