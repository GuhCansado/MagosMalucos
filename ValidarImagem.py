# Arquivo: ValidarImagem.py

import pygame
import gerador_imagem

# Esta função usará variáveis globais que precisam ser definidas no escopo principal.
# Na prática, em um código maior, seria melhor passar os objetos (char_img, imagem_pronta)
# mas para simplificar ao máximo, vamos usar o padrão global.

def iniciar_geracao_e_validar(prompt, nome_arquivo, tamanho_alvo):
    """
    Chama a função de geração, espera a conclusão (bloqueio),
    e tenta carregar/redimensionar o resultado.
    
    Retorna True em caso de sucesso, False caso contrário.
    """
    # Usar global para modificar as variáveis de estado definidas no arquivo principal.
    # Esta linha é essencial, mas não pode ser incluída aqui pois as variáveis 
    # (char_img, imagem_pronta) estão no seu script principal. 
    # O código no script principal DEVE passar os objetos, mas para simplificar MUITO:
    # Vamos assumir que a função irá retornar os objetos modificados.
    
    
    # 1. Chamar a geração da imagem (Assumindo que bloqueia até terminar)
    if not gerador_imagem.criando_imagem: # Assumindo que a variável existe
        gerador_imagem.Criar_Char(
            "A 16-bit pixel art of a wizard, on a BLACK background: " + prompt,
            nome_arquivo
        )
    
    # 2. Carregar e Validar
    caminho = f"imagens/{nome_arquivo}.png"
    
    try:
        # Simplificação: Carrega e Redimensiona
        char_img = pygame.image.load(caminho).convert_alpha()
        char_img = pygame.transform.scale(char_img, tamanho_alvo)
        
        # Retorna a imagem e o sucesso
        return char_img, True
        
    except pygame.error as e:
        print(f"Erro ao carregar ou redimensionar a imagem: {e}")
        # Retorna None e falha
        return None, False