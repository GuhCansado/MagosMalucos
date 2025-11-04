import pygame
import json

# Cores e Constantes
CINZA_SLOT = (100, 100, 100, 150)
COR_BORDA = (200, 200, 200)

class Slot(pygame.sprite.Sprite):
    """Slot para receber uma carta."""
    def __init__(self, x, y, largura, altura, numero_slot, raio_borda=10):
        super().__init__()
        self.largura, self.altura = largura, altura
        self.rect = pygame.Rect(x, y, largura, altura)
        self.carta = None 
        
        # Cria Surface com SRCALPHA para transparência
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(self.image, CINZA_SLOT, (0, 0, largura, altura), border_radius=raio_borda)
        pygame.draw.rect(self.image, COR_BORDA, (0, 0, largura, altura), width=2, border_radius=raio_borda)
        
        # Adiciona o número do slot
        fonte = pygame.font.Font(None, 24)
        texto = fonte.render(str(numero_slot), True, COR_BORDA)
        texto_rect = texto.get_rect(center=(largura // 2, altura // 2))
        self.image.blit(texto, texto_rect)


def inicializar_slots(screen, nivel):
    """
    Cria e posiciona os slots na parte inferior da tela com base no nível.
    Retorna a lista de objetos Slot.
    """
    tela_largura, tela_altura = screen.get_size()
    
    # Define a quantidade de slots
    num_elementos = 4 if nivel <= 5 else 8
    
    # Constantes de layout
    MARGEM_INFERIOR = 80
    slot_largura, slot_altura = 100, 130
    espacamento = 20
    pos_y_slots = tela_altura - MARGEM_INFERIOR - slot_altura
    
    # Cálculo para centralizar os slots
    largura_total = num_elementos * slot_largura + (num_elementos - 1) * espacamento
    start_x_slots = (tela_largura - largura_total) // 2
    
    slots = []
    for i in range(num_elementos):
        x = start_x_slots + i * (slot_largura + espacamento)
        slot = Slot(x, pos_y_slots, slot_largura, slot_altura, i + 1)
        slots.append(slot)
            
    return slots

def obter_lista_valores(slots):
    """
    Retorna a lista ordenada dos valores das cartas nos slots.
    Usado para enviar ao algoritmo de ordenação.
    """
    lista_valores = []
    for slot in slots:
        if slot.carta:
            lista_valores.append(slot.carta.valor)
    return lista_valores

def desenhar_slots(screen, slots):
    """Desenha todos os objetos Slot na tela."""
    for slot in slots:
        screen.blit(slot.image, slot.rect)