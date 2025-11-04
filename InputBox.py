# Arquivo: InputBox.py

import pygame

# Inicialização necessária (garante que a fonte funciona se for importada)
pygame.init() 

# Cores/Estilos
COLOR_INATIVO = pygame.Color('lightskyblue3')
COLOR_ATIVO = pygame.Color('dodgerblue2')
COLOR_TEXTO = pygame.Color(255, 255, 255)
FONTE = pygame.font.Font(None, 32) 

class InputBox:
    """
    Uma caixa de entrada de texto simples para Pygame.
    """
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INATIVO
        self.text = text
        self.final_text = ""
        self.active = False
        self.done = False

    def handle_event(self, event):
        """Processa eventos como clique do mouse e digitação de teclado."""
        if self.done:
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ATIVO if self.active else COLOR_INATIVO

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Finaliza a entrada, armazena o resultado e desativa.
                    self.final_text = self.text
                    self.done = True
                    self.active = False
                    # Opcional: print(f"Texto Final Inserido: {self.final_text}") 
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        """Desenha a caixa na superfície da tela."""
        # Renderiza o texto
        txt_surface = FONTE.render(self.text, True, COLOR_TEXTO)
        
        # Redimensiona o retângulo (largura mínima é a inicial)
        self.rect.w = max(self.rect.width, txt_surface.get_width() + 10)

        # Desenha o texto (com padding de 5px)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Desenha a borda do retângulo
        pygame.draw.rect(screen, self.color, self.rect, 2)