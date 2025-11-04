# cartas.py
import pygame
import json
import os # Para verificar se o arquivo existe e carregar imagens (simulado)
from interface import COR_PRETO, COR_BRANCO,COR_AMARELO ,criar_fonte

# Configuração Padrão da Carta
LARGURA_CARTA = 140
ALTURA_CARTA = 180

def carregar_dados_cartas():
    """Carrega os dados das cartas do arquivo JSON."""
    try:
        with open('cartas.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        print("ERRO: O arquivo 'cartas.json' não foi encontrado!")
        return []
    except json.JSONDecodeError:
        print("ERRO: O arquivo 'cartas.json' está mal formatado!")
        return []

class Carta:
    """Representa uma carta no jogo com valor, imagem e capacidade de arrasto."""
    def __init__(self, nome, caminho_imagem, valor, x=0, y=0):
        self.nome = nome
        self.valor = valor
        self.caminho_imagem = caminho_imagem
        
        # --- Simulação de Carregamento de Imagem ---
        # Como o Pygame pode falhar se a imagem não existir, vamos criar um
        # retângulo simples para a carta se a imagem não for encontrada.
        try:
            # Tenta carregar e redimensionar a imagem
            imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(imagem_original, (LARGURA_CARTA, ALTURA_CARTA))
        except pygame.error:
            # Se a imagem não for encontrada, cria um retângulo de cor sólida
            print(f"AVISO: Imagem {caminho_imagem} não encontrada. Usando substituto.")
            self.imagem = pygame.Surface((LARGURA_CARTA, ALTURA_CARTA))
            self.imagem.fill((100, 100, 100)) # Cor cinza
            # Adiciona o nome/valor no substituto
            fonte = criar_fonte(14)
            texto_nome = fonte.render(self.nome, True, COR_BRANCO)
            texto_valor = criar_fonte(20).render(str(self.valor), True, COR_BRANCO)
            self.imagem.blit(texto_nome, (5, 5))
            self.imagem.blit(texto_valor, (5, 25))
            
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.arrastando = False
        self.offset_x = 0
        self.offset_y = 0

    def desenhar(self, tela):

        tela.blit(self.imagem, self.rect)
        
        # Desenha o valor da carta na parte inferior (mesmo se tiver imagem)
        fonte = criar_fonte(40)
        texto_valor = fonte.render(str(self.valor), True,COR_AMARELO)
        
        # Posiciona o valor no centro inferior da carta
        posicao_valor = texto_valor.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
        tela.blit(texto_valor, posicao_valor)

    def iniciar_arrasto(self, pos):
        """Prepara a carta para ser arrastada."""
        if self.rect.collidepoint(pos):
            self.arrastando = True
            # Calcula o "offset" (diferença) para que o clique seja no ponto exato da carta
            self.offset_x = pos[0] - self.rect.x
            self.offset_y = pos[1] - self.rect.y
            return True
        return False

    def arrastar(self, pos):
        """Move a carta durante o arrasto."""
        if self.arrastando:
            self.rect.x = pos[0] - self.offset_x
            self.rect.y = pos[1] - self.offset_y

    def parar_arrasto(self):
        """Para o arrasto."""
        self.arrastando = False