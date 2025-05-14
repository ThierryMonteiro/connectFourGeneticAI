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
        # print("Vez do jogador 1")
        jogo.jogada(best_move(jogo,depth))
        ended, winner = jogo.hasEnded()
        if ended:
            if winner == 0:
                print("Empate!")
            else:
                print("Ganhador!")
                print(winner)
                jogo.imprimeTabuleiro()
            break
        # print("Vez do jogador 2")
        jogo.jogada(best_move(jogo,depth))
        ended, winner = jogo.hasEnded()
        if ended:
            if winner == 0:
                print("Empate!")
            else:
                print("Ganhador!")
                print(winner)
                jogo.imprimeTabuleiro()
            break


def utility(state):
    ended, winner = state.hasEnded()
    if ended:
        return 1 if winner == 1 else (-1 if winner == 2 else 0)

    # Heuristic: Check if Player 1 can win next move
    for col in range(state.largura):
        if col in state.actions():
            new_state = copy.deepcopy(state)
            new_state.jogada(col)
            _, winner = new_state.hasEnded()
            if winner == 1:
                return 0.9  # Almost a win for Player 1 (high threat)
            if winner == 2:
                return -0.9  # Almost a win for Player 2 (opportunity)

    return random.random()

def minmax(state, depth, maximizing_player, alpha =-float('inf'), beta = float('inf')):
    new_state = copy.deepcopy(state)
    ended, winner = state.hasEnded()
    if ended or depth == 0:
        #print Acabou o jogo ou a profundidade
        return utility(state)

    if not state.actions():
        #print Acabou as acoes
        return utility(state)

    if maximizing_player:
        max_eval = -float('inf')
        for action in new_state.actions():
            eval = minmax(new_state.jogada(action), depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        # print(f"Maximizing Player - Depth {depth}: {max_eval}")
        return max_eval
    else:
        min_eval = float('inf')

        for action in new_state.actions():
            eval = minmax(new_state.jogada(action), depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        # print(f"Maximizing Player - Depth {depth}: {min_eval}")

        return min_eval


def best_move(state, depth):
    is_maximizing = state.jogador == 1
    best_score = -float('inf') if is_maximizing else float('inf')
    best_action = None

    for action in state.actions():
        new_state = copy.deepcopy(state)
        new_state.jogada(action)
        score = minmax(new_state, depth - 1, not is_maximizing)

        if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
            best_score = score
            best_action = action

    return best_action

gameLoopIAs(Jogo(5,5), 4)