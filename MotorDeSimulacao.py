import time
from typing import List
from Ambiente import Ambiente
from Agente import Agente
from Acao import Acao, TipoAcao
from Posicao import Posicao
from Elemento import Elemento
from Parede import Parede
from Obstaculo import Obstaculo
from Farol import Farol

class MotorDeSimulacao:
    def __init__(self):
        self.agentes: List[Agente] = []
        self.ambiente: Ambiente = None

        self.passo_atual = 0
        self.max_passos = 5
        self.tempo_espera = 0.5 # segundos entre passos

    def cria(self, nome_do_ficheiro: str):
        self.agentes = []

        try:
            f = open(nome_do_ficheiro, 'r', encoding='utf-8')
            linhas = f.readlines()
            f.close()
        except FileNotFoundError:
            print(f"ERRO: O ficheiro '{nome_do_ficheiro}' não foi encontrado.")
            return

        altura = len(linhas)
        largura = len(linhas[0].rstrip('\n')) # remove o caracter invisível \n
        elementos: List[Elemento] = []

        for y, linha in enumerate(linhas):
            for x, e in enumerate(linha):
                if e == '\n':
                    continue
                pos = Posicao(x,y)
                if e == '#':
                    parede = Parede(pos)
                    elementos.append(parede)
                if e == 'F':
                    farol = Farol(pos)
                    elementos.append(farol)
                if e == 'A':
                    agente = Agente(100, pos)
                    elementos.append(agente)
                if e == 'O':
                    obstaculo = Obstaculo(pos)
                    elementos.append(obstaculo)

        self.ambiente = Ambiente(largura, altura, elementos)
        return

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        print(self.ambiente)

        ganhou = False

        while not ganhou and self.passo_atual < self.max_passos:
            self.passo_atual += 1
            # meter agentes a observar e a decidir ações

            # meter agente a agir

            # da print
            print(self.ambiente)
            time.sleep(self.tempo_espera)

            # verificar se ganhou
            if self.se_ganhou() == True:
                print("Ganhou!!")
                return


        if not ganhou:
            print("\n Perdeu: número máximo de passos atingidos.")
            return

    def se_ganhou(self):
        # falta adicionar para saída do labirinto
        for e in self.ambiente.elementos:
            if isinstance(e, Farol):
                farol = e
                break

        for a in self.agentes:
            if a.posicao.posicao_igual(farol.posicao):
                return True
        return False