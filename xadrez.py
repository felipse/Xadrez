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

# Cores e Fontes
BRANCO_CASA = (238, 238, 210)
PRETO_CASA = (118, 150, 86)
COR_DESTAQUE_SELECAO = (186, 202, 68)
COR_DESTAQUE_VALIDO = (100, 100, 100, 100)
COR_XEQUE = (255, 50, 50, 150)
FONTE_STATUS = pygame.font.SysFont('Arial', 50, True)


# --- CARREGANDO IMAGENS ---
# (Esta função não muda)
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
# (Todas as classes de peças permanecem as mesmas)
class Peca:
    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
    def desenhar(self, tela): pass
    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
    def get_movimentos_validos(self, tabuleiro): return []

class Peao(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_pawn"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        direcao = -1 if self.cor == 'w' else 1
        linha_inicial = 6 if self.cor == 'w' else 1
        if 0 <= self.linha + direcao < 8 and tabuleiro[self.linha + direcao][self.coluna] is None:
            movimentos.append((self.linha + direcao, self.coluna))
            if self.linha == linha_inicial and tabuleiro[self.linha + 2 * direcao][self.coluna] is None:
                movimentos.append((self.linha + 2 * direcao, self.coluna))
        for d_coluna in [-1, 1]:
            if 0 <= self.coluna + d_coluna < 8:
                peca_diagonal = tabuleiro[self.linha + direcao][self.coluna + d_coluna]
                if peca_diagonal is not None and peca_diagonal.cor != self.cor:
                    movimentos.append((self.linha + direcao, self.coluna + d_coluna))
        return movimentos

class Torre(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_rook"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        for d_linha, d_coluna in direcoes:
            for i in range(1, 8):
                linha_final = self.linha + d_linha * i
                coluna_final = self.coluna + d_coluna * i
                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    if peca_destino is None: movimentos.append((linha_final, coluna_final))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break 
                    else: break 
                else: break
        return movimentos

class Cavalo(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_knight"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        movimentos_em_L = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for d_linha, d_coluna in movimentos_em_L:
            linha_final, coluna_final = self.linha + d_linha, self.coluna + d_coluna
            if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                peca_destino = tabuleiro[linha_final][coluna_final]
                if peca_destino is None or peca_destino.cor != self.cor:
                    movimentos.append((linha_final, coluna_final))
        return movimentos

class Bispo(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_bishop"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
        for d_linha, d_coluna in direcoes:
            for i in range(1, 8):
                linha_final, coluna_final = self.linha + d_linha * i, self.coluna + d_coluna * i
                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    if peca_destino is None: movimentos.append((linha_final, coluna_final))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break 
                    else: break 
                else: break
        return movimentos

class Rainha(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_queen"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_linha, d_coluna in direcoes:
            for i in range(1, 8):
                linha_final, coluna_final = self.linha + d_linha * i, self.coluna + d_coluna * i
                if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                    peca_destino = tabuleiro[linha_final][coluna_final]
                    if peca_destino is None: movimentos.append((linha_final, coluna_final))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((linha_final, coluna_final))
                        break
                    else: break
                else: break
        return movimentos

class Rei(Peca):
    def desenhar(self, tela):
        img_key = f"{self.cor[0]}_king"
        tela.blit(IMAGENS[img_key], (self.coluna * TAMANHO_QUADRADO, self.linha * TAMANHO_QUADRADO))
    def get_movimentos_validos(self, tabuleiro):
        movimentos = []
        direcoes = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d_linha, d_coluna in direcoes:
            linha_final, coluna_final = self.linha + d_linha, self.coluna + d_coluna
            if 0 <= linha_final < 8 and 0 <= coluna_final < 8:
                peca_destino = tabuleiro[linha_final][coluna_final]
                if peca_destino is None or peca_destino.cor != self.cor:
                    movimentos.append((linha_final, coluna_final))
        return movimentos


# --- CLASSE PRINCIPAL DO JOGO ---
class Jogo:
    def __init__(self):
        # (O conteúdo de __init__ não muda)
        self.tabuleiro = []
        self.peca_selecionada = None
        self.turno = 'w'
        self.movimentos_validos = []
        self.pos_rei_w = (7, 4)
        self.pos_rei_b = (0, 4)
        self.game_over = False
        self.status_texto = ""
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        # (Não muda)
        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.tabuleiro[0] = [Torre(0,0,'b'), Cavalo(0,1,'b'), Bispo(0,2,'b'), Rainha(0,3,'b'), Rei(0,4,'b'), Bispo(0,5,'b'), Cavalo(0,6,'b'), Torre(0,7,'b')]
        self.tabuleiro[1] = [Peao(1, i, 'b') for i in range(8)]
        self.tabuleiro[6] = [Peao(6, i, 'w') for i in range(8)]
        self.tabuleiro[7] = [Torre(7,0,'w'), Cavalo(7,1,'w'), Bispo(7,2,'w'), Rainha(7,3,'w'), Rei(7,4,'w'), Bispo(7,5,'w'), Cavalo(7,6,'w'), Torre(7,7,'w')]

    def desenhar_tudo(self, tela):
        # (Não muda)
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

        if self.game_over:
            texto_surface = FONTE_STATUS.render(self.status_texto, True, pygame.Color('black'))
            pos_x = LARGURA // 2 - texto_surface.get_width() // 2
            pos_y = ALTURA // 2 - texto_surface.get_height() // 2
            pygame.draw.rect(TELA, pygame.Color('gray'), (pos_x - 10, pos_y - 10, texto_surface.get_width() + 20, texto_surface.get_height() + 20))
            TELA.blit(texto_surface, (pos_x, pos_y))

    def desenhar_movimentos_validos(self, tela):
        # (Não muda)
        for movimento in self.movimentos_validos:
            linha, coluna = movimento
            centro_x = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            centro_y = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
            pygame.draw.circle(tela, COR_DESTAQUE_VALIDO, (centro_x, centro_y), 15)
            
    def selecionar(self, linha, coluna):
        # (Não muda)
        if self.peca_selecionada:
            if self._mover(linha, coluna):
                self.trocar_turno()
            self.peca_selecionada = None
            self.movimentos_validos = []
        else:
            peca = self.tabuleiro[linha][coluna]
            if peca is not None and peca.cor == self.turno:
                self.peca_selecionada = peca
                movimentos_pseudo_legais = peca.get_movimentos_validos(self.tabuleiro)
                self.movimentos_validos = self._filtrar_movimentos_ilegais(peca, movimentos_pseudo_legais)
                return True
        return False
        
    def _mover(self, linha, coluna):
        if self.peca_selecionada and (linha, coluna) in self.movimentos_validos:
            pos_orig_l, pos_orig_c = self.peca_selecionada.linha, self.peca_selecionada.coluna
            
            if isinstance(self.peca_selecionada, Rei):
                if self.peca_selecionada.cor == 'w': self.pos_rei_w = (linha, coluna)
                else: self.pos_rei_b = (linha, coluna)

            self.tabuleiro[linha][coluna] = self.peca_selecionada
            self.tabuleiro[pos_orig_l][pos_orig_c] = None
            peca_movida = self.peca_selecionada
            peca_movida.mover(linha, coluna)
            
            # --- NOVO: Lógica de Promoção do Peão ---
            if isinstance(peca_movida, Peao):
                # Se um peão branco chega na linha 0 ou um peão preto na linha 7
                if (peca_movida.cor == 'w' and linha == 0) or \
                   (peca_movida.cor == 'b' and linha == 7):
                    # Promove para uma Rainha
                    self.tabuleiro[linha][coluna] = Rainha(linha, coluna, peca_movida.cor)
            
            return True
        return False

    def trocar_turno(self):
        # (Não muda)
        self.turno = 'b' if self.turno == 'w' else 'w'
        self.verificar_fim_de_jogo()

    # (Todos os outros métodos como verificar_fim_de_jogo, _get_todos_movimentos_legais, etc. não mudam)
    def verificar_fim_de_jogo(self):
        todos_os_movimentos = self._get_todos_movimentos_legais(self.turno)
        if len(todos_os_movimentos) == 0:
            self.game_over = True
            if self.is_in_check(self.turno):
                vencedor = "Brancas" if self.turno == 'b' else "Pretas"
                self.status_texto = f"Xeque-mate! {vencedor} vencem."
            else:
                self.status_texto = "Empate por Afogamento!"

    def _get_todos_movimentos_legais(self, cor):
        todos_os_movimentos = []
        for r in range(LINHAS):
            for c in range(COLUNAS):
                peca = self.tabuleiro[r][c]
                if peca is not None and peca.cor == cor:
                    movimentos_da_peca = peca.get_movimentos_validos(self.tabuleiro)
                    movimentos_legais_da_peca = self._filtrar_movimentos_ilegais(peca, movimentos_da_peca)
                    todos_os_movimentos.extend(movimentos_legais_da_peca)
        return todos_os_movimentos

    def _filtrar_movimentos_ilegais(self, peca, movimentos):
        movimentos_legais = []
        for movimento in movimentos:
            tabuleiro_temp = copy.deepcopy(self.tabuleiro)
            peca_temp = tabuleiro_temp[peca.linha][peca.coluna]
            l_final, c_final = movimento
            tabuleiro_temp[l_final][c_final] = peca_temp
            tabuleiro_temp[peca.linha][peca.coluna] = None
            pos_rei_temp = self.pos_rei_w if peca.cor == 'w' else self.pos_rei_b
            if isinstance(peca, Rei): pos_rei_temp = (l_final, c_final)
            cor_oponente = 'b' if peca.cor == 'w' else 'w'
            if not self.is_square_under_attack_temp(tabuleiro_temp, pos_rei_temp[0], pos_rei_temp[1], cor_oponente):
                movimentos_legais.append(movimento)
        return movimentos_legais
    
    def is_square_under_attack_temp(self, tabuleiro, linha, coluna, cor_atacante):
        for r in range(LINHAS):
            for c in range(COLUNAS):
                peca = tabuleiro[r][c]
                if peca is not None and peca.cor == cor_atacante:
                    peca.linha, peca.coluna = r, c
                    if isinstance(peca, Peao):
                        direcao = -1 if peca.cor == 'w' else 1
                        if (linha, coluna) in [(r + direcao, c - 1), (r + direcao, c + 1)]: return True
                    elif (linha, coluna) in peca.get_movimentos_validos(tabuleiro): return True
        return False

    def is_square_under_attack(self, linha, coluna, cor_atacante):
        return self.is_square_under_attack_temp(self.tabuleiro, linha, coluna, cor_atacante)

    def is_in_check(self, cor):
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
            # --- NOVO: Impede cliques se o jogo acabou ---
            if not jogo.game_over:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    linha, coluna = pos_y // TAMANHO_QUADRADO, pos_x // TAMANHO_QUADRADO
                    jogo.selecionar(linha, coluna)
        
        jogo.desenhar_tudo(TELA)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()