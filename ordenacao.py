import interface
import copy
import pygame 
import time

# --- Funções Auxiliares (mantidas) ---

def bubble_sort(lista):
    n = len(lista)
    lista_ordenada = copy.copy(lista) 
    
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lista_ordenada[j] > lista_ordenada[j + 1]:
                lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
    return lista_ordenada


# -------------------------------------------------------------
# NOVA TELA: tela_processamento_ordenacao (Substituindo processar_ordenacao)
# -------------------------------------------------------------
def tela_processamento_ordenacao(screen, lista_caixas_jogador, xp_atual, nivel_atual):

    """
    Retorna:
        tuple: (status_interno, novo_nivel, novo_xp_restante, proximo_estado_global)
    """
    
    # 1. PROCESSAMENTO DE DADOS (Cálculo de XP e Nível)
    lista_ordenada_correta = bubble_sort(lista_caixas_jogador)
    novo_xp = xp_atual
    mensagens_comparacao = []
    
    for i in range(len(lista_caixas_jogador)):
        valor_jogador = lista_caixas_jogador[i]
        valor_correto = lista_ordenada_correta[i]
        
        if valor_jogador == valor_correto:
            novo_xp += 5
            mensagens_comparacao.append(f"Posição {i}: Correta! (+5 XP)")
        else:
            novo_xp -= 1
            mensagens_comparacao.append(f"Posição {i}: Incorreta. (-1 XP)")

    novo_xp = max(0, novo_xp)
    xp_ganho_na_rodada = novo_xp - xp_atual
    novo_nivel = nivel_atual + (novo_xp // 10)
    xp_restante = novo_xp % 10

    mensagem_completa = "--- Processamento de Ordenação ---\n"
    mensagem_completa += f"Ordem Jogador: {lista_caixas_jogador}\n"
    mensagem_completa += f"Ordem Correta: {lista_ordenada_correta}\n\n"
    for msg in mensagens_comparacao:
        mensagem_completa += f"{msg}\n"
    mensagem_completa += f"\nXP Ganho: {xp_ganho_na_rodada}\n"
    mensagem_completa += f"Novo Nível: {novo_nivel}, XP: {xp_restante}"
    print(f"Processamento Completo:\n{mensagem_completa}")

    TELA_LARGURA, TELA_ALTURA = screen.get_size()
    tempo_inicio = pygame.time.get_ticks()
    duracao_ms = 8000
    relogio = pygame.time.Clock()

    while pygame.time.get_ticks() < tempo_inicio + duracao_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Retorna status de saída e os dados atuais
                return ("sair", nivel_atual, xp_atual, "sair") 
            if event.type == pygame.MOUSEBUTTONDOWN:
                return ("Ordenado", novo_nivel, xp_restante, "jogo")
        screen.fill(interface.COR_PRETO)
    
        interface.caixa_mensagem(
            screen,
            mensagem_completa,
            TELA_LARGURA // 2,
            TELA_ALTURA // 2,
            0 
        )
        
        pygame.display.flip()
        relogio.tick(60) 
    return ("Ordenado", novo_nivel, xp_restante, "jogo")
