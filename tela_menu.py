# tela_menu.py
import pygame
from interface import criar_fonte, COR_BRANCO, COR_PRETO, COR_AZUL_CLARO

def tela_menu(screen, estado_atual):
    """Desenha a tela de menu e processa os eventos."""
    TELA_LARGURA, TELA_ALTURA = screen.get_size()
    screen.fill((0, 0, 50)) # Fundo azul marinho
    
    fonte_titulo = criar_fonte(72)
    fonte_instrucao = criar_fonte(36)

    # Título
    titulo = fonte_titulo.render("MaGos MALucos", True, COR_BRANCO)
    titulo_pos = titulo.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 3))
    screen.blit(titulo, titulo_pos)
    
    # Instrução
    instrucao = fonte_instrucao.render("Pressione ESPAÇO para começar o Jogo", True, COR_AZUL_CLARO)
    instrucao_pos = instrucao.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2))
    screen.blit(instrucao, instrucao_pos)
    
    pygame.display.flip()
    
    # O Pygame_main já faz a checagem de eventos para mudar de estado (K_SPACE e QUIT).
    # Este menu não precisa de mais lógica de eventos, apenas desenhar.
    return estado_atual