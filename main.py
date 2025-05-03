from jogo import Jogo

# Tabuleiro é impresso no seu estado atual
# jogo inicia com o jogador 1, cujas peças são representadas por 1

def gameLoop(jogo):
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

gameLoop(Jogo(7, 7))
gameLoop(Jogo(4, 4))