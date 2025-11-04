import pygame
import sys
import jogo
import tela_menu 
import ordenacao


pygame.init()
pygame.display.set_caption("MaGos MALucos")

TELA_LARGURA, TELA_ALTURA = 800, 600
screen = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
rodando = True
estado = "menu" 
Nivel = 0
xp = 0

while rodando:
    proximo_estado = estado
    if estado == "menu":
        proximo_estado = tela_menu.tela_menu(screen, estado) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                proximo_estado = "sair"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                proximo_estado = "jogo"

    elif estado == "jogo":
        resultado_jogo = jogo.tela_jogo(screen, estado, xp)
        if isinstance(resultado_jogo, tuple) and resultado_jogo[0] == 'Pronto':
            _, Nivel_concluido, Lista_Caixas, _ = resultado_jogo
            
            print(f"Resultado do Nível {Nivel_concluido}: {Lista_Caixas}") 
            xp += 1
            
            proximo_estado = "menu" 
            
        else:
            proximo_estado = resultado_jogo

    elif estado == "sair":
        rodando = False
    estado = proximo_estado
    if estado == "sair":
        rodando = False
pygame.quit()
sys.exit()