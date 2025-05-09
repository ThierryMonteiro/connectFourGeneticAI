import random
from stringprep import b1_set

import jogo
from jogo import Jogo

import copy

# Tabuleiro é impresso no seu estado atual
# jogo inicia com o jogador 1, cujas peças são representadas por 1


infinity = 10000000000000000000

def gameLoopDoisHumanos(jogo):
    while True:
        jogo.imprimeTabuleiro()
        print("Vez do jogador 1")
        jogo.jogada()
        if jogo.hasEnded():
            break
        jogo.imprimeTabuleiro()
        print("Vez do jogador 2")
        jogo.jogada()
        if jogo.hasEnded():
            break

def gameLoopIAs(jogo, depth):
    while True:
        jogo.imprimeTabuleiro()
        print("Vez do jogador 1")
        jogo.jogada(best_move(jogo,depth))
        if jogo.hasEnded():
            break
        jogo.imprimeTabuleiro()
        print("Vez do jogador 2")
        jogo.jogada(best_move(jogo,depth))
        if jogo.hasEnded():
            break

def utility(state):
    if state.hasEnded():
        return infinity

def minmax(state, depth, maximizing_player):
    if (state.hasEnded()) or depth == 0:
        return utility(state)

    if maximizing_player:
        max_eval = -infinity
        for action in state.actions():
            state = copy.deepcopy(state)
            eval = minmax(state.jogada(action), depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = infinity
        for action in state.actions():
            state = copy.deepcopy(state)
            eval = minmax(state.jogada(action), depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(state, depth):
    best_action = None
    best_score = -float('inf')

    for action in state.actions():
        state = copy.deepcopy(state)
        new_state = state.jogada(action)
        score = minmax(new_state, depth - 1, False)
        if score > best_score:
            best_score = score
            best_action = action

    return best_action

gameLoopDoisHumanos(Jogo(5,5))

