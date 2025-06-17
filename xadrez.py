# xadrez.py

import pygame
import os
import copy

# --- CONFIGURAÇÕES INICIAIS ---
pygame.init()
LARGURA, ALTURA = 800, 800
LINHAS, COLUNAS = 8, 8
TAMANHO_QUADRADO = LARGURA // COLUNAS
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Xadrez")

# Cores
BRANCO_CASA = (238, 238, 210)
PRETO_CASA = (118, 150, 86)
COR_DESTAQUE_SELECAO = (186, 202, 68)
COR_DESTAQUE_VALIDO = (100, 100, 100, 100) # Cor para os círculos de movimentos válidos
COR_XEQUE = (255, 50, 50, 150) # Vermelho semi-transparente para o xeque

# --- CARREGANDO IMAGENS ---
def carregar_imagens():
    pecas_imgs = {}
    nomes_pecas = ["w_pawn", "w_rook", "w_knight", "w_bishop", "w_queen", "w_king",
                   "b_pawn", "b_rook", "b_knight", "b_bishop", "b_queen", "b_king"]
    for nome_arquivo in nomes_pecas:
        caminho = os.path.join("imagens", nome_arquivo + ".png")
        imagem = pygame.image.load(caminho).convert_alpha()
        pecas_imgs[nome_arquivo] = pygame.transform.scale(imagem, (TAMANHO_QUADRADO, TAMANHO_QUADRADO))
    return pecas_imgs

IMAGENS = carregar_imagens()


# --- CLASSES DAS PEÇAS ---
class Peca:
    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
    
    def desenhar(self, tela): pass

    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
    
    def get_movimentos_validos(self, tabuleiro):
        # Este método será sobrescrito por cada subclasse de peça
        return []

class Peao(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_pawn"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # A direção do movimento depende da cor do peão
        direcao = -1 if self.cor == 'w' else 1
        linha_inicial = 6 if self.cor == 'w' else 1

        # 1. Movimento simples para frente
        if 0 <= self.linha + direcao < 8 and tabuleiro[self.linha + direcao][self.coluna] is None:
            movimentos.append((self.linha + direcao, self.coluna))
            # 2. Movimento duplo inicial
            if self.linha == linha_inicial and tabuleiro[self.linha + 2 * direcao][self.coluna] is None:
                movimentos.append((self.linha + 2 * direcao, self.coluna))

        # 3. Capturas na diagonal
        for d_coluna in [-1, 1]:
            if 0 <= self.coluna + d_coluna < 8:
                peca_diagonal = tabuleiro[self.linha + direcao][self.coluna + d_coluna]
                if peca_diagonal is not None and peca_diagonal.cor != self.cor:
                    movimentos.append((self.linha + direcao, self.coluna + d_coluna))
        
        return movimentos

# Classes para as outras peças (ainda sem lógica de movimento)
class Torre(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_rook"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # Lista de tuplas representando as 4 direções: Cima, Baixo, Esquerda, Direita
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        for d_linha, d_coluna in direcoes:
            # Loop que "anda" na direção atual, uma casa de cada vez
            for i in range(1, 8):
                linha_final = self.linha + d_linha * i
                coluna_final = self.coluna + d_coluna * i

                # Verifica se a nova posição está dentro do tabuleiro
                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    
                    # Se a casa está vazia, é um movimento válido
                    if peca_destino is None:
                        movimentos.append((linha_final, coluna_final))
                    # Se a casa tem uma peça inimiga
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break # Para o loop nesta direção, pois a captura é o último movimento possível
                    # Se a casa tem uma peça da mesma cor
                    else:
                        break # Para o loop, pois a peça aliada bloqueia o caminho
                else:
                    break # Para o loop se a busca sair do tabuleiro
        
        return movimentos
           
class Cavalo(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_knight"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # Lista com todos os 8 movimentos possíveis em "L"
        movimentos_em_L = [
            (-2, -1), (-2, 1),  # 2 para cima, 1 para os lados
            (2, -1), (2, 1),   # 2 para baixo, 1 para os lados
            (-1, -2), (1, -2),  # 1 para os lados, 2 para cima/baixo (à esquerda)
            (-1, 2), (1, 2)    # 1 para os lados, 2 para cima/baixo (à direita)
        ]

        for d_linha, d_coluna in movimentos_em_L:
            linha_final = self.linha + d_linha
            coluna_final = self.coluna + d_coluna

            # 1. O movimento precisa estar dentro do tabuleiro
            if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                peca_destino = tabuleiro[linha_final][coluna_final]
                
                # 2. A casa de destino não pode ter uma peça da mesma cor
                if peca_destino is None or peca_destino.cor != self.cor:
                    movimentos.append((linha_final, coluna_final))
        
        return movimentos
    
class Bispo(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_bishop"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # As 4 direções diagonais
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 

        for d_linha, d_coluna in direcoes:
            for i in range(1, 8):
                linha_final = self.linha + d_linha * i
                coluna_final = self.coluna + d_coluna * i

                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    
                    if peca_destino is None:
                        movimentos.append((linha_final, coluna_final))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break 
                    else:
                        break 
                else:
                    break
        
        return movimentos
    
class Rainha(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_queen"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # Combinação das direções da Torre e do Bispo
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Retas (Torre)
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonais (Bispo)

        for d_linha, d_coluna in direcoes:
            for i in range(1, 8):
                linha_final = self.linha + d_linha * i
                coluna_final = self.coluna + d_coluna * i

                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    
                    if peca_destino is None:
                        movimentos.append((linha_final, coluna_final))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break 
                    else:
                        break 
                else:
                    break
        
        return movimentos
    
class Rei(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_king"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))

    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        # As mesmas 8 direções da Rainha, mas apenas uma casa de distância
        direcoes = [
            (-1, -1), (-1, 0), (-1, 1),  # Cima
            (0, -1), (0, 1),             # Lados
            (1, -1), (1, 0), (1, 1)      # Baixo
        ]

        for d_linha, d_coluna in direcoes:
            linha_final = self.linha + d_linha
            coluna_final = self.coluna + d_coluna

            # Lógica idêntica à do Cavalo: verifica se está no tabuleiro e se
            # a casa de destino não contém uma peça aliada.
            if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                peca_destino = tabuleiro[linha_final][coluna_final]
                if peca_destino is None or peca_destino.cor != self.cor:
                    movimentos.append((linha_final, coluna_final))
        
        return movimentos

# --- ESTADO DO JOGO ---
class Jogo:
    def __init__(self):
        self.tabuleiro = []
        self.peca_selecionada = None
        self.turno = 'w'
        self.movimentos_validos = []
        self.pos_rei_w = (7, 4)
        self.pos_rei_b = (0, 4)
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        # (O conteúdo deste método permanece o mesmo)
        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.tabuleiro[0] = [Torre(0,0,'b'), Cavalo(0,1,'b'), Bispo(0,2,'b'), Rainha(0,3,'b'), Rei(0,4,'b'), Bispo(0,5,'b'), Cavalo(0,6,'b'), Torre(0,7,'b')]
        self.tabuleiro[1] = [Peao(1, i, 'b') for i in range(8)]
        self.tabuleiro[6] = [Peao(6, i, 'w') for i in range(8)]
        self.tabuleiro[7] = [Torre(7,0,'w'), Cavalo(7,1,'w'), Bispo(7,2,'w'), Rainha(7,3,'w'), Rei(7,4,'w'), Bispo(7,5,'w'), Cavalo(7,6,'w'), Torre(7,7,'w')]

    def desenhar_tudo(self, tela):
        # (O conteúdo deste método permanece o mesmo)
        for r in range(LINHAS):
            for c in range(COLUNAS):
                cor = BRANCO_CASA if (r + c) % 2 == 0 else PRETO_CASA
                pygame.draw.rect(tela, cor, (c * TAMANHO_QUADRADO, r * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
        
        if self.is_in_check(self.turno):
            pos_rei = self.pos_rei_w if self.turno == 'w' else self.pos_rei_b
            r, c = pos_rei
            pygame.draw.rect(tela, COR_XEQUE, (c*TAMANHO_QUADRADO, r*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

        if self.peca_selecionada:
            r, c = self.peca_selecionada.linha, self.peca_selecionada.coluna
            pygame.draw.rect(tela, COR_DESTAQUE_SELECAO, (c*TAMANHO_QUADRADO, r*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
            self.desenhar_movimentos_validos(tela)
        
        for r in range(LINHAS):
            for c in range(COLUNAS):
                peca = self.tabuleiro[r][c]
                if peca is not None:
                    peca.desenhar(tela)

    def desenhar_movimentos_validos(self, tela):
        # (O conteúdo deste método permanece o mesmo)
        for movimento in self.movimentos_validos:
            linha, coluna = movimento
            centro_x = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            centro_y = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            pygame.draw.circle(tela, COR_DESTAQUE_VALIDO, (centro_x, centro_y), 15)
            
    def selecionar(self, linha, coluna):
        if self.peca_selecionada:
            if self._mover(linha, coluna):
                self.trocar_turno()
            self.peca_selecionada = None
            self.movimentos_validos = []
        else:
            peca = self.tabuleiro[linha][coluna]
            if peca is not None and peca.cor == self.turno:
                self.peca_selecionada = peca
                # --- LÓGICA ATUALIZADA ---
                # Pega os movimentos possíveis e depois filtra os que resultam em xeque
                movimentos_pseudo_legais = peca.get_movimentos_validos(self.tabuleiro)
                self.movimentos_validos = self._filtrar_movimentos_ilegais(peca, movimentos_pseudo_legais)
                return True
        return False
        
    def _mover(self, linha, coluna):
        if self.peca_selecionada and (linha, coluna) in self.movimentos_validos:
            pos_orig_l, pos_orig_c = self.peca_selecionada.linha, self.peca_selecionada.coluna
            if isinstance(self.peca_selecionada, Rei):
                if self.peca_selecionada.cor == 'w':
                    self.pos_rei_w = (linha, coluna)
                else:
                    self.pos_rei_b = (linha, coluna)
            self.tabuleiro[linha][coluna] = self.peca_selecionada
            self.tabuleiro[pos_orig_l][pos_orig_c] = None
            self.peca_selecionada.mover(linha, coluna)
            return True
        return False

    def _filtrar_movimentos_ilegais(self, peca, movimentos):
        """ Remove da lista de movimentos aqueles que deixariam o rei em xeque. """
        movimentos_legais = []
        for movimento in movimentos:
            # Simula o movimento em uma cópia do tabuleiro
            tabuleiro_temp = copy.deepcopy(self.tabuleiro)
            peca_temp = tabuleiro_temp[peca.linha][peca.coluna]

            # Move a peça na cópia
            l_final, c_final = movimento
            tabuleiro_temp[l_final][c_final] = peca_temp
            tabuleiro_temp[peca.linha][peca.coluna] = None
            
            # Atualiza a posição do rei na cópia se o rei foi movido
            pos_rei_temp = self.pos_rei_w if peca.cor == 'w' else self.pos_rei_b
            if isinstance(peca, Rei):
                pos_rei_temp = (l_final, c_final)
            
            # Verifica se o movimento resultou em xeque para si mesmo
            cor_oponente = 'b' if peca.cor == 'w' else 'w'
            if not self.is_square_under_attack_temp(tabuleiro_temp, pos_rei_temp[0], pos_rei_temp[1], cor_oponente):
                movimentos_legais.append(movimento)
        
        return movimentos_legais

    def is_square_under_attack_temp(self, tabuleiro, linha, coluna, cor_atacante):
        """ Versão da função que opera em um tabuleiro temporário. """
        for r in range(LINHAS):
            for c in range(COLUNAS):
                peca = tabuleiro[r][c]
                if peca is not None and peca.cor == cor_atacante:
                    # Atualiza a posição da peça temporariamente para gerar movimentos corretos
                    peca.linha, peca.coluna = r, c
                    if isinstance(peca, Peao):
                        direcao = -1 if peca.cor == 'w' else 1
                        if (linha, coluna) in [(r + direcao, c - 1), (r + direcao, c + 1)]:
                            return True
                    elif (linha, coluna) in peca.get_movimentos_validos(tabuleiro):
                        return True
        return False

    def trocar_turno(self):
        # (O conteúdo deste método permanece o mesmo)
        self.turno = 'b' if self.turno == 'w' else 'w'

    def is_square_under_attack(self, linha, coluna, cor_atacante):
        # (O conteúdo deste método permanece o mesmo - pode ser removido no futuro se não for mais usado diretamente)
        return self.is_square_under_attack_temp(self.tabuleiro, linha, coluna, cor_atacante)

    def is_in_check(self, cor):
        # (O conteúdo deste método permanece o mesmo)
        pos_rei = self.pos_rei_w if cor == 'w' else self.pos_rei_b
        cor_oponente = 'b' if cor == 'w' else 'w'
        return self.is_square_under_attack(pos_rei[0], pos_rei[1], cor_oponente)

# --- LOOP PRINCIPAL ---
def main():
    rodando = True
    clock = pygame.time.Clock()
    jogo = Jogo()
    while rodando:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                linha, coluna = pos_y // TAMANHO_QUADRADO, pos_x // TAMANHO_QUADRADO
                jogo.selecionar(linha, coluna)
        
        jogo.desenhar_tudo(TELA)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()