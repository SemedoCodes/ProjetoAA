# ProjetoAA
Implementação do Projeto da Cadeira de Agentes Autónomos
Realizado por:
Marcos Nascimento - 4º ano de Informática e Gestão de Empresas
Luana Lopes (110702) - 4º ano de Informática e Gestão de Empresas

**Guia de utilização:**

Siga os passos abaixo para configurar e executar a simulação.

1. Configurar a simulação

    A configuração é feita através de ficheiros de texto que definem o cenário e o comportamento dos agentes. 

    Pode utilizar um dos ficheiros de exemplo já existentes ou criar o seu próprio ficheiro com os seguintes parâmetros:

| Parâmetro      | Opções/Exemplos                                                                                 | Descrição                                                                                                  |
|----------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| tipo_problema  | Farol, Labirinto                                                                                | Problema a executar                                                                                        |
| tipo_politica  | PoliticaFixa, PoliticaAprendizagem                                                              | PoliticaFixa serve para o modo burro ou de teste, PoliticaAprendizagem o agente aprende usando o Q-Learning |
| mapa_ficheiro  | Farol_1 (simples), Farol_2 (inclui obstáculos), Labirinto_1 (1 Agente), Labirinto_2 (2 Agentes) | Ficheiro que contém o desenho do mapa                                                                      
| max_passos     | Ex: 100 ou 500                                                                                  | Limite de passos antes de terminar o episódio                                                              |
| ficheiro_teste | Ex_qtable_agente_1.txt                                                                          | Para modo teste, carrega uma memória pré-treinada                                                          |

2. Inicializar o motor no main.py

   motor = MotorDeSimulacao.cria( nome_do_ficheiro)

Após a execução, o simulador gera os seguintes ficheiros para análise:
- relatório.csv: Histórico detalhado de todos os episódios (Passos, Vitória/Derrota, Recompensa)
- qtable_agente_X.txt: A Tabela Q aprendida pelo agente, que pode ser reutilizada em testes.
   
   
