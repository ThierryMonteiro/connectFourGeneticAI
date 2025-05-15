import copy
import random
from jogo import Jogo

def avaliacao_personalizada(jogo, pesos):
    w1, w2, w3 = pesos
    jogador = 1  # Avaliamos do ponto de vista do jogador 1 sempre

    # Características:
    linhas_abertas = contar_linhas_abertas(jogo, jogador)
    trincas = contar_trincas(jogo, jogador)
    controle_centro = contar_centro(jogo, jogador)

    return w1 * linhas_abertas + w2 * trincas + w3 * controle_centro

def contar_linhas_abertas(jogo, jogador):
    cont = 0
    tab = jogo.estado
    altura = jogo.altura
    largura = jogo.largura
    adversario = 2 if jogador == 1 else 1

    # horizontal
    for i in range(altura):
        for j in range(largura - 3):
            trecho = [tab[i][j + k] for k in range(4)]
            if adversario not in trecho:
                cont += 1

    # vertical
    for i in range(altura - 3):
        for j in range(largura):
            trecho = [tab[i + k][j] for k in range(4)]
            if adversario not in trecho:
                cont += 1

    # diagonal principal
    for i in range(altura - 3):
        for j in range(largura - 3):
            trecho = [tab[i + k][j + k] for k in range(4)]
            if adversario not in trecho:
                cont += 1

    # diagonal secundária
    for i in range(3, altura):
        for j in range(largura - 3):
            trecho = [tab[i - k][j + k] for k in range(4)]
            if adversario not in trecho:
                cont += 1

    return cont



def contar_trincas(jogo, jogador):
    cont = 0
    tab = jogo.estado
    altura = jogo.altura
    largura = jogo.largura

    def conta_trecho(trecho):
        return trecho.count(jogador) == 3 and trecho.count(0) == 1

    # horizontal
    for i in range(altura):
        for j in range(largura - 3):
            trecho = [tab[i][j + k] for k in range(4)]
            if conta_trecho(trecho):
                cont += 1

    # vertical
    for i in range(altura - 3):
        for j in range(largura):
            trecho = [tab[i + k][j] for k in range(4)]
            if conta_trecho(trecho):
                cont += 1

    # diagonal principal
    for i in range(altura - 3):
        for j in range(largura - 3):
            trecho = [tab[i + k][j + k] for k in range(4)]
            if conta_trecho(trecho):
                cont += 1

    # diagonal secundária
    for i in range(3, altura):
        for j in range(largura - 3):
            trecho = [tab[i - k][j + k] for k in range(4)]
            if conta_trecho(trecho):
                cont += 1

    return cont

def contar_centro(jogo, jogador):
    meio = jogo.largura // 2
    colunas = [meio]
    if jogo.largura % 2 == 0:
        colunas.append(meio - 1)

    cont = 0
    for linha in jogo.estado:
        for c in colunas:
            if linha[c] == jogador:
                cont += 1
    return cont

def melhor_jogada_com_pesos(state, depth, pesos):
    is_maximizing = state.jogador == 1
    best_score = -float('inf') if is_maximizing else float('inf')
    best_action = None

    for action in state.actions():
        new_state = copy.deepcopy(state)
        new_state.jogada(action)
        score = minmax_avaliacao(new_state, depth - 1, not is_maximizing, pesos)

        if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
            best_score = score
            best_action = action

    return best_action

def minmax_avaliacao(state, depth, maximizing_player, pesos, alpha=-float('inf'), beta=float('inf')):
    ended, winner = state.hasEnded()
    if ended or depth == 0:
        return avaliacao_personalizada(state, pesos)

    if maximizing_player:
        max_eval = -float('inf')
        for action in state.actions():
            new_state = copy.deepcopy(state)
            new_state.jogada(action)
            eval = minmax_avaliacao(new_state, depth - 1, False, pesos, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for action in state.actions():
            new_state = copy.deepcopy(state)
            new_state.jogada(action)
            eval = minmax_avaliacao(new_state, depth - 1, True, pesos, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
