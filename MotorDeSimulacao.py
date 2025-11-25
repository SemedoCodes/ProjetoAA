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
        self.max_passos = 100
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
                if e == '_' or e == '|':
                    parede = Parede(pos)
                    elementos.append(parede)
                if e == 'F':
                    farol = Farol(pos)
                    elementos.append(pos)
                if e == 'A':
                    agente = Agente(100, pos)
                    elementos.append(agente)
                if e == 'O':
                    obstaculo = Obstaculo(pos)
                    elementos.append(pos)

        self.ambiente = Ambiente(largura, altura, elementos)
        print(self.ambiente)
        return
