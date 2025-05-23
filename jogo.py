class Jogo():
    def __init__(self,altura,largura):
        self.jogador = 1 # 1 é o jogador 1, o jogador 2 é 2
        self.estado = self.criaTabuleiro(altura, largura)
        self.turno = 0 # counter de turno
        self.altura = altura
        self.largura = int(largura)
        self.ultimaJogada = 0 # ultima jogada feita, usada para otimizar a busca de condicoes de vitória

    def criaTabuleiro(self, altura, largura):

        tabuleiro = []

        for i in range(altura):
            tabuleiro.append([])
            for j in range(largura):
                tabuleiro[i].append(0)

        return tabuleiro

    def imprimeTabuleiro(self):
        print("Tabuleiro atual:")
        for i in range(len(self.estado)):
            print(self.estado[i])
        print("\n")
        return True


    def jogada(self, coluna=None):

        if coluna is None:
            print("Em qual coluna você quer jogar?")
            coluna = int(input())

        # While para verificar se a coluna existe e é possivel jogar nela
        while coluna < 0 or coluna >= len(self.estado[0]) or (self.estado[0][coluna] != 0):
            print("Coluna inválida, tente novamente.")
            coluna = int(input())

        self.ultimaJogada = [self.findLastZero(coluna), coluna]
        self.estado[self.findLastZero(coluna)][coluna] = self.jogador

        self.turno += 1
        self.jogador = 2 if self.jogador == 1 else 1
        return self

    def findLastZero(self, coluna): # retorna a linha do último zero na coluna

        for i in range(len(self.estado)-1, -1, -1):
            if self.estado[i][coluna] == 0:
                return i
        return -1 # se não houver zero, retorna -1

    def hasEnded(self):

        if self.ultimaJogada is None:
            return False, None  # Jogo não terminou porque não houve jogadas

        # Verifica se há 4 peças em linha, baseadas na última jogada

        verificaJogador = 2 if self.jogador == 1 else 1

        # Verifica na horizontal
        for i in range(self.largura-3):
            if self.estado[self.ultimaJogada[0]][i] == verificaJogador and \
                    self.estado[self.ultimaJogada[0]][i+1] == verificaJogador and \
                    self.estado[self.ultimaJogada[0]][i+2] == verificaJogador and \
                    self.estado[self.ultimaJogada[0]][i+3] == verificaJogador:
                # print("Jogador " + str(verificaJogador) + " ganhou fazendo uma jogada na coluna " + str(self.ultimaJogada[1]))
                return True, verificaJogador

        # Verifica na vertical
        for i in range(self.altura-3):
            if self.estado[i][self.ultimaJogada[1]] == verificaJogador and \
                    self.estado[i+1][self.ultimaJogada[1]] == verificaJogador and \
                    self.estado[i+2][self.ultimaJogada[1]] == verificaJogador and \
                    self.estado[i+3][self.ultimaJogada[1]] == verificaJogador:
                # print("Jogador " + str(verificaJogador) + " ganhou fazendo uma jogada na coluna " + str(self.ultimaJogada[1]))
                return True,verificaJogador


        # Verifica na diagonal principal
        for i in range(self.altura-3):
            for j in range(self.largura-3):
                if self.estado[i][j] == verificaJogador and \
                        self.estado[i+1][j+1] == verificaJogador and \
                        self.estado[i+2][j+2] == verificaJogador and \
                        self.estado[i+3][j+3] == verificaJogador:
                    # print("Jogador " + str(verificaJogador) + " ganhou fazendo uma jogada na coluna " + str(
                    #    self.ultimaJogada[1]))
                    return True,verificaJogador

        # Verifica na diagonal secundária

        for i in range(3, self.altura):
            for j in range(self.largura-3):
                if self.estado[i][j] == verificaJogador and \
                        self.estado[i-1][j+1] == verificaJogador and \
                        self.estado[i-2][j+2] == verificaJogador and \
                        self.estado[i-3][j+3] == verificaJogador:
                    # print("Jogador " + str(verificaJogador) + " ganhou fazendo uma jogada na coluna " + str(
                    #    self.ultimaJogada[1]))
                    return True,verificaJogador


        # Verifica se o tabuleiro está cheio depois de verificar condições de vitoria

        if all(self.estado[0][j] != 0 for j in range(len(self.estado[0]))):
            return True, 0

        return False, None

    def actions(self):
        return [i for i in range(self.largura) if self.estado[0][i] == 0]



