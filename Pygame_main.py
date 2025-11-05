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
Nivel = 1
xp = 0
# ---------------------------------

while rodando:
    proximo_estado = estado
    
    # Lógica de Menu
    if estado == "menu":
        proximo_estado = tela_menu.tela_menu(screen, estado) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                proximo_estado = "sair"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                proximo_estado = "jogo"

    # jogo --------------------
    elif estado == "jogo":
        resultado_jogo = jogo.tela_jogo(screen, estado, Nivel)
        
        if isinstance(resultado_jogo, tuple) and resultado_jogo[0] == 'Pronto':
            #(Pronto, Nivel_concluido, Lista_Caixas, Proximo_Estado)
            _, Nivel_concluido, Lista_Caixas, estado_seguinte = resultado_jogo
            #print(f"Resultado do Nível {Nivel_concluido}: {Lista_Caixas}") 
            status_interno, novo_nivel, novo_xp_restante, proximo_estado = ordenacao.tela_processamento_ordenacao(
                screen, Lista_Caixas, xp, Nivel
            )
            Nivel = novo_nivel
            xp = novo_xp_restante 
            print(f"Estado Atualizado: Nível={Nivel}, XP={xp}")
            proximo_estado = proximo_estado

        else:
            proximo_estado = resultado_jogo

    #QUIT
    elif estado == "sair":
        rodando = False
        
    estado = proximo_estado
    
    if estado == "sair":
        rodando = False
        
pygame.quit()
sys.exit()