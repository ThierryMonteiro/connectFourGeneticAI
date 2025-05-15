import random
from stringprep import b1_set

import jogo
from jogo import Jogo

import copy

from ag import *
from minmax import avaliacao_personalizada
from jogo import Jogo

infinity = 10000000000000000000

# Tabuleiro é impresso no seu estado atual
# jogo inicia com o jogador 1, cujas peças são representadas por 1

if __name__ == "__main__":
    
    melhor_individuo = algoritmo_genetico(
        num_geracoes=15,
        tamanho_populacao=5,
        taxa_crossover=0.8,
        taxa_mutacao=0.8,
        range_pesos=(0.4, 0.7)
    )
    print("Melhor conjunto de pesos encontrado:", melhor_individuo)
