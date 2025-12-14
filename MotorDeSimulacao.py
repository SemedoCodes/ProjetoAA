import time
from typing import List, Dict, Optional, Any, Tuple
from Ambiente import Ambiente
from Agente import Agente
from Accao import Accao
from Posicao import Posicao
from Elemento import Elemento
from Parede import Parede
from Obstaculo import Obstaculo
from Farol import Farol
from AgenteSimples import AgenteSimples
from Saida import Saida
from Simulador import Simulador
import threading
import time

class MotorDeSimulacao(Simulador):
    def __init__(self):
        self.agentes: List[Agente] = []
        self.ambiente: Ambiente = None

        self.passo_atual = 0
        self.max_passos = 100 # por defeito
        self.tempo_espera = 0.0 # segundos entre passos

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

        num_participantes = len(self.agentes) + 1
        barreira = threading.Barrier(num_participantes)

        # Configurar Agentes para Threads
        posicoes_iniciais = {}
        for a in self.agentes:
            posicoes_iniciais[a] = Posicao(a.posicao.x, a.posicao.y)
            # Injetar dependências para o agente funcionar sozinho
            if hasattr(a, 'set_sincronizacao'):
                a.set_sincronizacao(self.ambiente, barreira)
            # Definir como Daemon (para fecharem se o programa principal fechar)
            a.daemon = True

        historico_global = []
        num_eps = 350

        if self.agentes and self.agentes[0].politica and self.agentes[0].politica.nome == "Política Fixa":
            num_eps = 1

        for a in self.agentes:
            if not a.is_alive():
                a.start()

        # ciclo de episódios
        for ep in range(1, num_eps + 1):
            print(f"Inicio do episódio: {ep}" )
            self.passo_atual = 0
            ganhou = False

            for a in self.agentes:
                p_ini = posicoes_iniciais[a]
                a.posicao = Posicao(p_ini.x, p_ini.y)

                # Reset da memória de mensagens
                if hasattr(a, 'mensagens_recebidas'):
                    a.mensagens_recebidas = []

                # Reset do histórico de posições
                if hasattr(a, 'historico_recente'):
                    a.historico_recente = []

                a.recompensa_acumulada = 0.0

            while not ganhou and self.passo_atual < self.max_passos:
                self.passo_atual += 1

                try:
                    barreira.wait()
                except threading.BrokenBarrierError:
                    print("Erro de sincronização: Barreira quebrada.")
                    break

                self.ambiente.atualizacao()

                if self.tempo_espera > 0:
                    time.sleep(self.tempo_espera)

                # verificar se ganhou
                if self.se_ganhou() == True:
                    print(self.ambiente)
                    ganhou = True
                    print("Ganhou!!")
                    print(f"Episódio {ep}: Ganhou em {self.passo_atual} passos.")

            if not ganhou:
                print(self.ambiente)
                print(f"Episódio {ep}: perdeu - número máximo de passos atingidos.")

            # registo dos dados
            for a in self.agentes:
                dados_ep = {
                    "episodio": ep,
                    "agente_id": a.id,
                    "passos": self.passo_atual,
                    "ganhou": 1 if ganhou else 0,
                    "recompensa_total": round(a.recompensa_acumulada, 2)
                }
                historico_global.append(dados_ep)
            self.exportar_relatorio(historico_global, "relatorio.csv")

        for a in self.agentes:
            if hasattr(a, 'parar'):
                a.parar()  # Sinaliza à thread para sair do loop

            if a.politica and hasattr(a.politica, 'guardar_politica'):
                nome_ficheiro = f"qtable_agente_{a.id}.txt"
                a.politica.guardar_politica(nome_ficheiro)
                print(f"Política do Agente {a.id} guardada em '{nome_ficheiro}'.")

            # Libertar a barreira final para as threads terminarem
        try:
            barreira.reset()
        except:
            pass

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

    def exportar_relatorio(self, dados: List[Dict], nome_ficheiro: str):
        try:
            with open(nome_ficheiro, 'w', encoding='utf-8') as f:
                f.write("Episodio,AgenteID,Passos,Ganhou,Recompensa\n")

                for linha in dados:
                    f.write(
                        f"{linha['episodio']},{linha['agente_id']},{linha['passos']},{linha['ganhou']},{linha['recompensa_total']}\n")
        except Exception as e:
            print(f"Erro ao gravar relatório: {e}")