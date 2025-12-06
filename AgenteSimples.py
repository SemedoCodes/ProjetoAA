from Agente import Agente
from Acao import Acao, TipoAcao
from Posicao import Posicao

class AgenteSimples(Agente):
    def __init__(self, id_agente: int, posicao: Posicao):
        super().__init__(id_agente, posicao)

    def cria(nome_do_ficheiro_parametros: str) -> 'AgenteSimples':
        novo_agente = AgenteSimples(1, Posicao(0, 0))
        return novo_agente

    def age(self) -> Acao:
        if self.ultima_observacao is None or self.politica is None:
            return Acao(TipoAcao.FAZER_NADA)
        acao = self.politica.selecionar_acao(self.ultima_observacao)

        return acao

