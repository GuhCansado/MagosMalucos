import pygame
import random
import os 

from cartas import Carta, carregar_dados_cartas, LARGURA_CARTA, ALTURA_CARTA
from interface import Slot, Botao, caixa_mensagem, criar_fonte, COR_BRANCO, COR_AMARELO, COR_PRETO

# --- Configurações / Constantes ---
LISTA_VALORES_PROIBIDOS_1 = [1, 2, 3, 7, 8, 9] 
LISTA_VALORES_PROIBIDOS_2 = [4, 5, 6, 10, 11, 12]

PROIBICOES = {}
for v in LISTA_VALORES_PROIBIDOS_1:
    PROIBICOES[v] = LISTA_VALORES_PROIBIDOS_2
for v in LISTA_VALORES_PROIBIDOS_2:
    PROIBICOES[v] = LISTA_VALORES_PROIBIDOS_1

valores_verificados1 = None
valores_verificados2 = None

NUM_SLOTS = 4
ESPACO_SLOTS = 10
X_MAO = 50
Y_MAO = 50

def verificar_proibicao_adjacencia(slots):
    global valores_verificados1, valores_verificados2
    valores_nos_slots = [s.valor_slot if s.valor_slot else None for s in slots]

    for i in range(len(valores_nos_slots) - 1):
        a, b = valores_nos_slots[i], valores_nos_slots[i + 1]
        if a is None or b is None:
            continue
        if a in PROIBICOES and b in PROIBICOES[a]:
            valores_verificados1 = a
            valores_verificados2 = b
            return True
    
    valores_verificados1 = None
    valores_verificados2 = None
    return False

def criar_nova_carta_aleatoria(todos_dados_cartas, x, y):
    if not todos_dados_cartas:
        return None
    dados = random.choice(todos_dados_cartas)
    return Carta(
        nome=dados['nome'],
        caminho_imagem=dados['caminho_imagem'],
        valor=dados['valor'],
        x=x, y=y
    )

def gerar_mao_aleatoria(todos_dados_cartas, largura_carta, espaco, x_mao=X_MAO, y_mao=Y_MAO, quantidade=4):
    cartas = []
    for i in range(quantidade):
        x = x_mao + i * (largura_carta + espaco)
        c = criar_nova_carta_aleatoria(todos_dados_cartas, x, y_mao)
        if c:
            cartas.append(c)
    return cartas

# --- Tela de Jogo (Principal) ---
def tela_jogo(screen, estado_atual, nivel):
    TODOS_DADOS_CARTAS = carregar_dados_cartas()
    if not TODOS_DADOS_CARTAS:
        return "menu"

    TELA_LARGURA, TELA_ALTURA = screen.get_size()

    largura_total_slots = (LARGURA_CARTA * NUM_SLOTS) + (ESPACO_SLOTS * (NUM_SLOTS - 1))
    x_inicial = (TELA_LARGURA - largura_total_slots) // 2
    y_slots = TELA_ALTURA - 190

    # --- Adição: Slot com suporte a pilha ---
    class SlotPilha:
        def __init__(self, x, y, largura, altura):
            self.rect = pygame.Rect(x, y, largura, altura)
            self.cartas_pilhadas = []

        def colocar_carta(self, carta):
            self.cartas_pilhadas = [carta]
            carta.rect.topleft = self.rect.topleft

        def empilhar_carta(self, carta):
            if len(self.cartas_pilhadas) < 2:
                self.cartas_pilhadas.append(carta)
                # desloca um pouco a segunda carta pra dar efeito visual
                carta.rect.topleft = (self.rect.x + 10 * len(self.cartas_pilhadas), self.rect.y + 10 * len(self.cartas_pilhadas))
                return True
            return False

        def desenhar(self, screen):
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
            for carta in self.cartas_pilhadas:
                carta.desenhar(screen)

        @property
        def valor_slot(self):
            return sum(carta.valor for carta in self.cartas_pilhadas) if self.cartas_pilhadas else None

        @property
        def carta_colocada(self):
            return self.cartas_pilhadas[-1] if self.cartas_pilhadas else None

    SLOTS = [SlotPilha(x_inicial + i * (LARGURA_CARTA + ESPACO_SLOTS), y_slots, LARGURA_CARTA, ALTURA_CARTA)
             for i in range(NUM_SLOTS)]

    cartas_na_mao = gerar_mao_aleatoria(TODOS_DADOS_CARTAS, LARGURA_CARTA, ESPACO_SLOTS)
    
    botao_novas_cartas = Botao(10, 10, 150, 40, "+ Cartas")
    botao_finalizar = Botao(TELA_LARGURA - 160, y_slots - 60, 150, 40, "Finalizar Jogada")

    carta_sendo_arrastada = None
    slot_original_da_carta = None
    tempo_fim_mensagem_proibida = 0
    fonte_nivel = criar_fonte(36)
    rodando_jogo = True

    # --- Lógica de Layout e Devolução---
    def recalcular_layout_mao():
        for i, c in enumerate(cartas_na_mao):
            c.rect.topleft = (X_MAO + i * (LARGURA_CARTA + ESPACO_SLOTS), Y_MAO)

    def devolver_carta_para_mao(carta):
        if carta not in cartas_na_mao:
             cartas_na_mao.append(carta)
             
    recalcular_layout_mao()
    
    # --- Loop Principal do Jogo ---
    while rodando_jogo:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            
            match event.type:
                case pygame.QUIT:
                    return "sair"
                
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if botao_novas_cartas.verificar_clique(event):
                            cartas_na_mao.clear() 
                            cartas_na_mao.extend(gerar_mao_aleatoria(TODOS_DADOS_CARTAS, LARGURA_CARTA, ESPACO_SLOTS))
                            recalcular_layout_mao()
                            continue

                        slots_cheios = all(s.valor_slot for s in SLOTS)
                        if slots_cheios and botao_finalizar.verificar_clique(event):
                            if verificar_proibicao_adjacencia(SLOTS):
                                caixa_mensagem(screen, f"IMPOSSÍVEL! {valores_verificados1} e {valores_verificados2} não podem estar juntos!", TELA_LARGURA // 2, TELA_ALTURA // 2, 2000)
                                tempo_fim_mensagem_proibida = pygame.time.get_ticks() + 2000
                            else:
                                valores_slots = [s.valor_slot for s in SLOTS]
                                for s in SLOTS:
                                    s.cartas_pilhadas.clear()
                                return ('Pronto', nivel, valores_slots, 'menu') 
                        
                        # Iniciar drag
                        if not carta_sendo_arrastada:
                            for carta in reversed(cartas_na_mao):
                                if carta.iniciar_arrasto(mouse_pos):
                                    carta_sendo_arrastada, slot_original_da_carta = carta, None
                                    break
                            if not carta_sendo_arrastada:
                                for slot in SLOTS:
                                    if slot.carta_colocada and slot.carta_colocada.iniciar_arrasto(mouse_pos):
                                        carta_sendo_arrastada, slot_original_da_carta = slot.carta_colocada, slot
                                        slot.cartas_pilhadas.remove(slot.carta_colocada)
                                        break

                case pygame.MOUSEMOTION:
                    if carta_sendo_arrastada:
                        carta_sendo_arrastada.arrastar(event.pos)

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1 and carta_sendo_arrastada:
                        carta_sendo_arrastada.parar_arrasto()
                        soltou_em_alvo = False
                        
                        for slot in SLOTS:
                            if slot.rect.colliderect(carta_sendo_arrastada.rect):

                                if nivel >= 2 and slot.carta_colocada is not None:
                                    if slot.empilhar_carta(carta_sendo_arrastada):
                                        if carta_sendo_arrastada in cartas_na_mao:
                                            cartas_na_mao.remove(carta_sendo_arrastada)
                                        soltou_em_alvo = True
                                        break

                                carta_alvo_no_slot = slot.carta_colocada
                                
                                if carta_alvo_no_slot is None:
                                    slot.colocar_carta(carta_sendo_arrastada)
                                    if slot_original_da_carta is None and carta_sendo_arrastada in cartas_na_mao:
                                        cartas_na_mao.remove(carta_sendo_arrastada) 
                                else:
                                    slot.colocar_carta(carta_sendo_arrastada)
                                    if slot_original_da_carta:
                                        slot_original_da_carta.colocar_carta(carta_alvo_no_slot)
                                    else:
                                        devolver_carta_para_mao(carta_alvo_no_slot)
                                    if slot_original_da_carta is None and carta_sendo_arrastada in cartas_na_mao:
                                        cartas_na_mao.remove(carta_sendo_arrastada)
                                
                                soltou_em_alvo = True
                                break
                        
                        # Devolver para a origem se não houver alvo
                        if not soltou_em_alvo and slot_original_da_carta:
                            slot_original_da_carta.colocar_carta(carta_sendo_arrastada)
                        
                        # Limpeza
                        carta_sendo_arrastada = None
                        slot_original_da_carta = None
                        recalcular_layout_mao() 

        # --- Desenho ---
        screen.fill((0, 0, 0))
        
        texto_nivel = fonte_nivel.render(f"NÍVEL: {nivel}", True, COR_BRANCO)
        screen.blit(texto_nivel, (TELA_LARGURA - texto_nivel.get_width() - 10, 10))

        for slot in SLOTS:
            slot.desenhar(screen)

        for carta in cartas_na_mao:
             carta.desenhar(screen)

        botao_novas_cartas.desenhar(screen)
        if all(s.valor_slot for s in SLOTS):
            botao_finalizar.desenhar(screen)

        if carta_sendo_arrastada:
            carta_sendo_arrastada.desenhar(screen)

        if tempo_fim_mensagem_proibida > pygame.time.get_ticks():
            caixa_mensagem(screen, f"IMPOSSÍVEL! {valores_verificados1} e {valores_verificados2} não podem estar juntos!", TELA_LARGURA // 2, TELA_ALTURA // 2, 0)

        pygame.display.flip()
