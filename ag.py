import random
import copy
import time

from minmax import *
from multiprocessing import Pool
seed = 44
###########################
##### multiprocessing #####
def fitness_wrapper_torneio(args):
    individuo, populacao, seed = args
    random.seed(seed)
    return fitness_torneio(individuo, populacao)

def avaliar_populacao_torneio(populacao):
    seeds = [i for i in range(len(populacao))]
    with Pool() as pool:
        resultados = pool.map(
            fitness_wrapper_torneio,
            [(ind, populacao, seed) for ind, seed in zip(populacao, seeds)]
        )
    return resultados
##### multiprocessing #####
###########################

def gerar_individuo_base(weight_range=(0.4, 0.7)):
    return [random.uniform(*weight_range) for _ in range(3)]


def fitness_torneio(individuo, populacao, n=10):
    vitorias = 0
    oponentes = random.sample(populacao, min(n, len(populacao)))
    for i, oponente in enumerate(oponentes):
        if individuo == oponente:
            continue  # evita jogar contra si mesmo

        jogo = Jogo(5, 5)
        vencedor = simula_jogo(jogo, individuo, oponente)

        if vencedor == 1:
            vitorias += 1
        elif vencedor == 0:
            vitorias += 0.5
        
    return vitorias / n



def simula_jogo(jogo, pesos_agente1, pesos_agente2, profundidade=4):
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
    return [
        pai1[i] if random.random() > taxa_crossover else pai2[i]
        for i in range(len(pai1))
    ]


def mutacao(individuo, taxa_mutacao, range_pesos=(-2, 2)):
    return [
        min(range_pesos[1], max(range_pesos[0], w + random.uniform(-0.1 * abs(w) - 0.01, 0.1 * abs(w) + 0.01)))
        if random.random() < taxa_mutacao else w
        for w in individuo
    ]



def selecao_por_torneio(populacao, fitnesses, k=3):
    selecionados = random.sample(list(zip(populacao, fitnesses)), k)
    selecionados.sort(key=lambda x: x[1], reverse=True)
    return selecionados[0][0]  # retorna o indivíduo com maior fitness




def algoritmo_genetico(num_geracoes, tamanho_populacao, taxa_crossover, taxa_mutacao, range_pesos):
    populacao = [gerar_individuo_base(range_pesos) for _ in range(tamanho_populacao)]

    historico = []

    # Inicializa o melhor global com o primeiro individuo da população e seu fitness (zero por enquanto)
    melhor_geral = None
    melhor_fitness_geral = -float('inf')  # -infinito para garantir que qualquer fitness seja maior

    for gen in range(num_geracoes):
        print(f"🔥 Geração {gen+1}/{num_geracoes}")
        inicio = time.time()
        fitnesses = avaliar_populacao_torneio(populacao)
        elite = copy.deepcopy(populacao[fitnesses.index(max(fitnesses))])
        nova_pop = [elite]  # mantém o melhor da geração anterior

        while len(nova_pop) < tamanho_populacao:
            pai1 = selecao_por_torneio(populacao, fitnesses, 3)
            pai2 = selecao_por_torneio(populacao, fitnesses, 3)
            filho = crossover_uniforme(pai1, pai2, taxa_crossover)
            filho = mutacao(filho, taxa_mutacao, range_pesos)
            nova_pop.append(filho)

        populacao = nova_pop
        melhor = max(fitnesses)

        # Atualiza o melhor global se a geração atual tem melhor fitness
        if melhor > melhor_fitness_geral:
            melhor_fitness_geral = melhor
            melhor_geral = copy.deepcopy(populacao[fitnesses.index(melhor)])

        fim = time.time()
        print(f"⏱️ Tempo da geração: {fim - inicio:.2f} segundos")
        print(f"💪 Geração {gen+1}: melhor fitness = {melhor}\n")
        historico.append(melhor)

    # Retorna o melhor indivíduo encontrado em toda a execução
    return melhor_geral, historico
