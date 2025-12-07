import time
from typing import List, Dict, Type, Optional, Any, Tuple
from Ambiente import Ambiente
from Agente import Agente
from Accao import Acao, TipoAccao
from Posicao import Posicao
from Elemento import Elemento
from Parede import Parede
from Obstaculo import Obstaculo
from Farol import Farol
from AgenteSimples import AgenteSimples
from Saida import Saida

class MotorDeSimulacao:
    def __init__(self):
        self.agentes: List[Agente] = []
        self.ambiente: Ambiente = None

        self.passo_atual = 0
        self.max_passos = 100 # por defeito
        self.tempo_espera = 0.5 # segundos entre passos

    # cria e inicializa a instância da classe apartir do ficheiro de parametros
    @classmethod
    def cria(cls, nome_do_ficheiro_parametros: str) -> 'MotorDeSimulacao':
        novo_motor = cls()
        parametros: Dict[str, Any] = {}
        mapa_ficheiro: Optional[str] = None

        # ler o ficheiro
        try:
            with open(nome_do_ficheiro_parametros, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha or linha.startswith('#'): continue

                    chave, valor = linha.split('=', 1)
                    chave = chave.strip()
                    valor = valor.strip()
                    parametros[chave] = valor
        except FileNotFoundError:
            print(f"ERRO: O ficheiro de parâmetros '{nome_do_ficheiro_parametros}' não foi encontrado.")
            return novo_motor

        # criar o motor
        mapa_ficheiro = parametros.get('mapa_ficheiro')

        if 'max_passos' in parametros:
            try:
                novo_motor.max_passos = int(parametros['max_passos'])
            except ValueError:
                print("Aviso: max_passos inválido. Usando valor padrão (100).")

        if not mapa_ficheiro:
            print("ERRO: Parâmetro 'mapa_ficheiro' não especificado.")
            return novo_motor

        try:
            with open(mapa_ficheiro, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print(f"ERRO: O ficheiro de mapa '{mapa_ficheiro}' não foi encontrado.")
            return novo_motor

        altura = len(linhas)
        largura = len(linhas[0].rstrip('\n')) # remove o caracter invisível \n
        elementos: List[Elemento] = []

        for y, linha in enumerate(linhas):
            for x, e in enumerate(linha):
                if e == '\n':
                    continue
                pos = Posicao(x,y)
                if e == '#':
                    elementos.append(Parede(pos))
                elif e == 'F':
                    elementos.append(Farol(pos))
                elif e == 'O':
                    elementos.append(Obstaculo(pos))
                elif e == 'S':
                    elementos.append(Saida(pos))
                elif e == 'A':
                    agente = AgenteSimples.cria(nome_do_ficheiro_parametros)
                    agente.configura_ambiente(
                        id_agente=len(novo_motor.agentes) + 1,
                        posicao_inicial=pos
                    )
                    elementos.append(agente)
                    novo_motor.agentes.append(agente)

        novo_motor.ambiente = Ambiente(largura, altura, elementos)
        return novo_motor

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        if self.ambiente is None:
            print("ERRO DE EXECUÇÃO: O Ambiente não foi inicializado corretamente. Verifique os ficheiros de mapa.")
            return

        print(self.ambiente)
        ganhou = False

        while not ganhou and self.passo_atual < self.max_passos:
            self.passo_atual += 1
            acoes_e_observacoes: Dict[Agente, Tuple[Acao, Any]] = {}

            self.ambiente.atualizacao()

            for a in self.agentes:
                obs = self.ambiente.observacaoPara(a)
                a.observacao(obs)
                acao = a.age()

                acoes_e_observacoes[a] = (acao, obs)

            for a, (acao, obs_anterior) in acoes_e_observacoes.items():
                recompensa = self.ambiente.agir(acao, a)
                a.avaliacaoEstadoAtual(recompensa)

                obs_nova = self.ambiente.observacaoPara(a)

                a.observacao(obs_nova)

            # atualizar a grelha
            print(self.ambiente)
            time.sleep(self.tempo_espera)

            # verificar se ganhou
            if self.se_ganhou() == True:
                print("Ganhou!!")
                return

        if not ganhou:
            print("\n Perdeu: número máximo de passos atingidos.")

    def se_ganhou(self):
        objetivo = None
        for e in self.ambiente.elementos:
            if isinstance(e, Farol) or isinstance(e, Saida):
                objetivo = e
                break

        if objetivo is None:
            return False

        for a in self.agentes:
            if a.posicao == objetivo.posicao:
                return True
        return False