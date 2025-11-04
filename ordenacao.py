# ordenacao.py
import copy

def bubble_sort(lista):
    """Implementa o algoritmo Bubble Sort."""
    n = len(lista)
    # Copia a lista para evitar modificar a original durante a ordenação
    lista_ordenada = copy.copy(lista) 
    
    for i in range(n - 1):
        # O último i elementos já estão no lugar
        for j in range(0, n - i - 1):
            # Troca se o elemento encontrado for maior que o próximo
            if lista_ordenada[j] > lista_ordenada[j + 1]:
                lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
    return lista_ordenada

def processar_ordenacao(lista_caixas_jogador, xp_atual, nivel_atual):
    """
    Processa a lista de cartas do jogador, calcula XP e Nível.

    Args:
        lista_caixas_jogador (list): A lista de valores de cartas na ordem do jogador.
        xp_atual (int): O valor de XP atual do jogador.
        nivel_atual (int): O nível atual do jogador.

    Retorna:
        tuple: (status, nova_lista_ordenada, novo_nivel, proximo_estado)
    """
    
    # 1. Cria a cópia da lista e ordena usando Bubble Sort
    lista_ordenada_correta = bubble_sort(lista_caixas_jogador)
    
    novo_xp = xp_atual
    
    print("\n--- Processamento de Ordenação ---")
    print(f"Ordem do Jogador: {lista_caixas_jogador}")
    print(f"Ordem Correta:   {lista_ordenada_correta}")
    
    # 2. Compara as listas e calcula o XP
    for i in range(len(lista_caixas_jogador)):
        valor_jogador = lista_caixas_jogador[i]
        valor_correto = lista_ordenada_correta[i]
        
        if valor_jogador == valor_correto:
            # Carta no local CERTO: +5 XP
            novo_xp += 5
            print(f"  Posição {i}: Correta! (+5 XP)")
        else:
            # Carta no local ERRADO: -1 XP
            novo_xp -= 1
            print(f"  Posição {i}: Incorreta. (-1 XP)")

    # Garante que o XP não fique negativo
    novo_xp = max(0, novo_xp)
    
    # 3. Avanço de Nível (a cada 10 de XP)
    xp_ganho_na_rodada = novo_xp - xp_atual
    print(f"XP Ganho na rodada: {xp_ganho_na_rodada}")
    
    novo_nivel = nivel_atual + (novo_xp // 10)
    
    # Atualiza o XP restante para o próximo nível (XP % 10)
    xp_restante = novo_xp % 10

    print(f"Nível Atualizado: {novo_nivel}, XP Restante: {xp_restante}")

    # Retorna o status, a lista correta (opcional), o novo nível e o XP restante, e o próximo estado.
    return ("Ordenado", lista_ordenada_correta, novo_nivel, xp_restante, "jogo")