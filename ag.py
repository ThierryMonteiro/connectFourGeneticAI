import random
import copy
from minmax import *
from multiprocessing import Pool

###########################
##### multiprocessing #####
def fitness_wrapper_torneio(args):
    individuo, populacao = args
    return fitness_torneio(individuo, populacao)

def avaliar_populacao_torneio(populacao):
    with Pool() as pool:
        resultados = pool.map(fitness_wrapper_torneio, [(ind, populacao) for ind in populacao])
    return resultados
##### multiprocessing #####
###########################

def fitness_torneio(individuo, populacao, n=10):
    vitorias = 0
    oponentes = random.sample(populacao, min(n, len(populacao)))
    ultimo_jogo = Jogo(5, 5)
    for i, oponente in enumerate(oponentes):
        if individuo == oponente:
            continue  # evita jogar contra si mesmo

        jogo = Jogo(5, 5)
        vencedor = simula_jogo(jogo, individuo, oponente)
        ultimo_jogo = copy.deepcopy(jogo)

        if vencedor == 1:
            vitorias += 1
        elif vencedor == 0:
            vitorias += 0.5
        
    # jogo.imprimeTabuleiro()
    return vitorias / n



def simula_jogo(jogo, pesos_agente1, pesos_agente2, profundidade=3):
    while True:
        if jogo.jogador == 1:
            acao = melhor_jogada_com_pesos(jogo, profundidade, pesos_agente1)
        else:
            acao = melhor_jogada_com_pesos(jogo, profundidade, pesos_agente2)

        jogo.jogada(acao)
        fim, vencedor = jogo.hasEnded()
        if fim:
            return vencedor

def crossover_uniforme(pai1, pai2, taxa_crossover):
    if random.random() > taxa_crossover:
        return pai1[:]  # sem crossover
    filho = []
    for w1, w2 in zip(pai1, pai2):
        filho.append(random.choice([w1, w2]))
    return filho

def mutacao(individuo, taxa_mutacao):
    import random
    return [
        w + random.uniform(-1.5, 1.5) if random.random() < taxa_mutacao else w
        for w in individuo
    ]

def selecao_por_torneio(populacao, fitnesses, k=3):
    import random
    selecionados = random.sample(list(zip(populacao, fitnesses)), k)
    selecionados.sort(key=lambda x: x[1], reverse=True)
    return selecionados[0][0]  # retorna o indivíduo com maior fitness


def algoritmo_genetico(num_geracoes, tamanho_populacao, taxa_crossover, taxa_mutacao):
    import random

    # população inicial
    populacao = [[random.uniform(-2, 2) for _ in range(3)] for _ in range(tamanho_populacao)]
    print(populacao)

    historico = []

    for gen in range(num_geracoes):
        fitnesses = avaliar_populacao_torneio(populacao)
        nova_pop = []

        while len(nova_pop) < tamanho_populacao:
            pai1 = selecao_por_torneio(populacao, fitnesses, 2)
            pai2 = selecao_por_torneio(populacao, fitnesses, 2)
            filho = crossover_uniforme(pai1, pai2, taxa_crossover)
            filho = mutacao(filho, taxa_mutacao)
            nova_pop.append(filho)

        populacao = nova_pop
        melhor = max(fitnesses)

        ### o valor do fitness é o número de vitórias em relação ao número de jogos
        ### um fitness 1.0 significa que o indivíduo venceu todos os jogos
        ### um fitness 0.5 significa que o indivíduo venceu metade dos jogos
        print(f"Geração {gen}: melhor fitness = {melhor}")
        historico.append(melhor)

    fitnesses = avaliar_populacao_torneio(populacao)
    melhor_individuo = populacao[fitnesses.index(max(fitnesses))]

    return melhor_individuo
