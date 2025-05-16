from ag import *

if __name__ == "__main__":
    
    melhor_individuo = algoritmo_genetico(
        num_geracoes=50,
        tamanho_populacao=15,
        taxa_crossover=0.8,
        taxa_mutacao=0.1,
        range_pesos=(-1,1)
    )
    print("Melhor conjunto de pesos encontrado:", melhor_individuo)
