# classes.py

import pygame

class Peca:
    """
    Classe base para todas as peças do xadrez.
    """
    def __init__(self, linha, coluna, cor, imagens_pecas):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor  # 'branca' ou 'preta'
        self.imagem = None
        self.nome = ''

    def desenhar(self, tela, tamanho_quadrado):
        """ Desenha a peça na tela. """
        tela.blit(self.imagem, (self.coluna * tamanho_quadrado, self.linha * tamanho_quadrado))

    def mover(self, linha, coluna):
        """ Atualiza a posição da peça. """
        self.linha = linha
        self.coluna = coluna

# Exemplo de como serão as outras classes (ainda não vamos usá-las)
# class Peao(Peca):
#     def __init__(self, linha, coluna, cor, imagens_pecas):
#         super().__init__(linha, coluna, cor)
#         self.nome = 'peao'
#         self.imagem = imagens_pecas[cor[0] + '_' + self.nome] # ex: 'b_peao'