# interface.py
import pygame

# --- Configurações Comuns ---
COR_BRANCO = (255, 255, 255)
COR_PRETO = (0, 0, 0)
COR_CINZA_CLARO = (200, 200, 200)
COR_AZUL_CLARO = (150, 150, 255)
COR_AMARELO = (255, 255, 0)
# --- Funções de Interface ---

def criar_fonte(tamanho):
    """Cria e retorna um objeto de fonte do Pygame."""
    try:
        # Tenta carregar uma fonte padrão do sistema
        return pygame.font.Font(None, tamanho)
    except:
        # Se falhar, usa a fonte padrão do Pygame
        return pygame.font.SysFont('Arial', tamanho)

class Botao:
    """Classe simples para criar um botão clicável."""
    def __init__(self, x, y, largura, altura, texto, cor_fundo=COR_AZUL_CLARO, cor_texto=COR_BRANCO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = criar_fonte(24)
        self.clicado = False 

    def desenhar(self, tela):
        """Desenha o botão na tela."""
        # Desenha o fundo do botão
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=5)
        
        # Renderiza e centraliza o texto
        superficie_texto = self.fonte.render(self.texto, True, self.cor_texto)
        posicao_texto = superficie_texto.get_rect(center=self.rect.center)
        tela.blit(superficie_texto, posicao_texto)

    def verificar_clique(self, evento):
        """Verifica se o botão foi clicado."""
        self.clicado = False # Reseta o estado a cada verificação
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.clicado = True
        return self.clicado

class Slot:
    """Classe simples para representar um slot onde uma carta pode ser colocada."""
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
        self.carta_colocada = None  # Objeto da Carta que está neste slot

    def desenhar(self, tela):
        """Desenha o slot na tela."""
        # Desenha uma borda simples para o slot
        pygame.draw.rect(tela, COR_CINZA_CLARO, self.rect, 2)
        
        # Se tiver uma carta, desenha a carta
        if self.carta_colocada:
            self.carta_colocada.desenhar(tela)

    def colocar_carta(self, carta):
        """Coloca uma carta no slot e ajusta sua posição."""
        self.carta_colocada = carta
        # Centraliza a carta no slot
        self.carta_colocada.rect.center = self.rect.center

    def remover_carta(self):
        """Remove a carta do slot e retorna ela."""
        carta = self.carta_colocada
        self.carta_colocada = None
        return carta

def caixa_mensagem(tela, mensagem, x, y, duracao_ms):
    """
    Desenha uma caixa de texto temporária para mensagens.
    Retorna o tempo que a mensagem deve desaparecer.
    """
    COR_FUNDO_MENSAGEM = (255, 100, 100) # Vermelho claro
    fonte = criar_fonte(28)
    superficie_texto = fonte.render(mensagem, True, COR_PRETO)
    
    # Cria um retângulo de fundo um pouco maior que o texto
    rect_fundo = superficie_texto.get_rect(center=(x, y))
    rect_fundo = rect_fundo.inflate(20, 10) # Aumenta 20 de largura e 10 de altura
    
    # Desenha o fundo e a borda
    pygame.draw.rect(tela, COR_FUNDO_MENSAGEM, rect_fundo, border_radius=5)
    pygame.draw.rect(tela, COR_PRETO, rect_fundo, 2, border_radius=5)
    
    # Desenha o texto
    tela.blit(superficie_texto, superficie_texto.get_rect(center=(x, y)))
    
    # Retorna o tempo em milissegundos que a mensagem deve desaparecer
    return pygame.time.get_ticks() + duracao_ms

# Você pode adicionar mais classes/funções de interface aqui (Ex: BotaoAjuda)
# Exemplo de um Botão que mostra uma caixa de texto (simulado)
class BotaoAjuda(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 40, "Ajuda")
        self.ajuda_visivel = False
        self.texto_ajuda = "Arraste as cartas para os slots, mas cuidado com os valores proibidos lado a lado!"

    def desenhar(self, tela):
        super().desenhar(tela)
        if self.ajuda_visivel:
            # Simula a caixa de texto de ajuda (pode ser melhorado)
            fonte = criar_fonte(18)
            superficie_texto = fonte.render(self.texto_ajuda, True, COR_PRETO)
            
            x_ajuda = self.rect.left
            y_ajuda = self.rect.bottom + 5
            
            rect_fundo = superficie_texto.get_rect(topleft=(x_ajuda + 5, y_ajuda + 5)).inflate(10, 10)
            
            pygame.draw.rect(tela, COR_CINZA_CLARO, rect_fundo, border_radius=3)
            pygame.draw.rect(tela, COR_PRETO, rect_fundo, 1, border_radius=3)
            tela.blit(superficie_texto, (x_ajuda + 10, y_ajuda + 10))

    def verificar_clique(self, evento):
        clicou = super().verificar_clique(evento)
        if clicou:
            self.ajuda_visivel = not self.ajuda_visivel # Inverte o estado da ajuda
        return clicou