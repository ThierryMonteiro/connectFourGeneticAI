from ag import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    melhor_individuo, historico = algoritmo_genetico(
        num_geracoes=20,
        tamanho_populacao=15,
        taxa_crossover=0.8,
        taxa_mutacao=0.1,
        range_pesos=(-1,1)
    )
    print("Melhor conjunto de pesos encontrado:", melhor_individuo)

    # Plotando o gráfico da evolução do fitness
    plt.plot(historico)
    plt.xlabel('Geração')
    plt.ylabel('Melhor Fitness')
    plt.title('Evolução do Fitness ao longo das Gerações')
    plt.grid(True)
    plt.show()
