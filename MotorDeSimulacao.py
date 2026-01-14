import time
from typing import List, Dict, Optional, Any
from Ambiente import Ambiente
from Agente import Agente
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

    """
    Gere o ciclo de vida da simulação.
    Responsável por sincronizar os turnos entre agentes e ambiente.
    """
    def __init__(self):
        self.agentes: List[Agente] = []
        self.ambiente: Ambiente = None
        self.passo_atual = 0
        self.max_passos=350
        self.tempo_espera = 0.0 # segundos entre passos

    # Cria e inicializa a classe apartir do ficheiro de parametros
    @classmethod
    def cria(cls, nome_do_ficheiro_parametros: str) -> 'MotorDeSimulacao':
        novo_motor = cls()
        parametros: Dict[str, Any] = {}

        # Leitura dos parâmetros
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

        # Configuração
        novo_motor.max_passos = int(parametros.get('max_passos', 350))
        mapa_ficheiro = parametros.get('mapa_ficheiro')

        if not mapa_ficheiro:
            print("ERRO: Parâmetro 'mapa_ficheiro' não especificado.")
            return novo_motor

        # Leitura do mapa e criação de elementos
        try:
            with open(mapa_ficheiro, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print(f"ERRO: O ficheiro de mapa '{mapa_ficheiro}' não foi encontrado.")
            return novo_motor

        elementos: List[Elemento] = []
        altura = len(linhas)
        largura = len(linhas[0].rstrip('\n'))

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
                    # Cria o agente
                    agente = AgenteSimples.cria(nome_do_ficheiro_parametros)
                    agente.configura_ambiente(id_agente=len(novo_motor.agentes) + 1, posicao_inicial=pos)
                    elementos.append(agente)
                    novo_motor.agentes.append(agente)

        novo_motor.ambiente = Ambiente(largura, altura, elementos)
        return novo_motor

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        # Gere Episódios -> Passos -> Sincronização
        if self.ambiente is None:
            print("ERRO DE EXECUÇÃO: O Ambiente não foi inicializado corretamente.")
            return

        # Sincronização: N agentes + 1 motor
        barreira = threading.Barrier(len(self.agentes) + 1)

        # Inicialização das Threads dos agentes
        posicoes_iniciais = {}
        for a in self.agentes:
            posicoes_iniciais[a] = Posicao(a.posicao.x, a.posicao.y)
            if hasattr(a, 'set_sincronizacao'):
                a.set_sincronizacao(self.ambiente, barreira)
            a.daemon = True
            if not a.is_alive():
                a.start()

        historico_global = []
        num_eps = 350

        # Ajuste de número de episódios na Política Fixa
        if self.agentes and self.agentes[0].politica and self.agentes[0].politica.nome == "Política Fixa":
            num_eps = 1

        # CICLO DE EPISÓDIOS
        for ep in range(1, num_eps + 1):
            print(f"Inicio do episódio: {ep}" )
            self.passo_atual = 0
            ganhou = False
            self.ambiente.rasto.clear()

            # Reset do estado dos agentes para uma nova tentativa
            for a in self.agentes:
                p_ini = posicoes_iniciais[a]
                a.posicao = Posicao(p_ini.x, p_ini.y)
                a.recompensa_acumulada = 0.0
                if hasattr(a, 'mensagens_recebidas'):
                    a.mensagens_recebidas = []
                if hasattr(a, 'historico_recente'):
                    a.historico_recente = []

            # CICLO DE PASSOS
            while not ganhou and self.passo_atual < self.max_passos:
                self.passo_atual += 1

                # Esperar que todos os agentes decidam a sua ação
                try:
                    barreira.wait()
                except threading.BrokenBarrierError:
                    break

                # Motor atualiza o mundo
                self.ambiente.atualizacao()
                # print(self.ambiente)

                if self.tempo_espera > 0:
                    time.sleep(self.tempo_espera)

                # Verificar vitória
                if self.se_ganhou() == True:
                    print(self.ambiente)
                    ganhou = True
                    print("Ganhou!!")
                    print(f"Episódio {ep}: Ganhou - {self.passo_atual} passos.")

            if not ganhou:
                print(self.ambiente)
                print(f"Episódio {ep}: Perdeu - número máximo de passos atingidos.")

            # FIM DO EPISÓDIO
            # Atualizar Epsilon
            for a in self.agentes:
                if hasattr(a, 'fim_do_episodio'):
                    a.fim_do_episodio()

            # Registo dos dados
            for a in self.agentes:
                historico_global.append({
                    "episodio": ep,
                    "agente_id": a.id,
                    "passos": self.passo_atual,
                    "ganhou": 1 if ganhou else 0,
                    "recompensa_total": round(a.recompensa_acumulada, 2)
                })
            self.exportar_relatorio(historico_global, "relatorio.csv")

        # FIM DO CICLO DE EPISÓDIOS
        for a in self.agentes:
            if hasattr(a, 'parar'):
                a.parar()
            if a.politica and hasattr(a.politica, 'guardar_politica'):
                a.politica.guardar_politica(f"qtable_agente_{a.id}.txt")

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
        if objetivo is None: return False
        for a in self.agentes:
            if a.posicao == objetivo.posicao: return True
        return False

    def exportar_relatorio(self, dados: List[Dict], nome_ficheiro: str):
        try:
            with open(nome_ficheiro, 'w', encoding='utf-8') as f:
                f.write("Episodio,AgenteID,Passos,Vitória,Recompensa\n")
                for linha in dados:
                    f.write(f"{linha['episodio']},{linha['agente_id']},{linha['passos']},{linha['ganhou']},{linha['recompensa_total']}\n")
        except Exception as e:
            print(f"Erro ao gravar relatório: {e}")