import pygame
import random

from cartas import Carta, carregar_dados_cartas, LARGURA_CARTA, ALTURA_CARTA
from interface import Slot, Botao, caixa_mensagem, criar_fonte, COR_BRANCO, BotaoAjuda

# ----------------------------
# Configurações / constantes
# ----------------------------
LISTA_VALORES_PROIBIDOS_1 = [1, 2, 3, 7, 8, 9]  # coringas removidos conforme pediu
LISTA_VALORES_PROIBIDOS_2 = [4, 5, 6, 10, 11, 12]

PROIBICOES = {}
for v in LISTA_VALORES_PROIBIDOS_1:
    PROIBICOES[v] = LISTA_VALORES_PROIBIDOS_2
for v in LISTA_VALORES_PROIBIDOS_2:
    PROIBICOES[v] = LISTA_VALORES_PROIBIDOS_1

# Estado global (colocados no topo)
valores_verificados1 = None
valores_verificados2 = None

# Layout / gameplay
NUM_SLOTS = 4
ESPACO_SLOTS = 10
X_MAO = 50
Y_MAO = 50

# ----------------------------
# Funções utilitárias
# ----------------------------
def verificar_proibicao_adjacencia(slots):
    """Retorna True se houver par proibido adjacente; também atualiza globals
    valores_verificados1/2 com os dois valores que violaram a regra."""
    global valores_verificados1, valores_verificados2
    valores_nos_slots = [s.carta_colocada.valor if s.carta_colocada else None for s in slots]

    for i in range(len(valores_nos_slots) - 1):
        a = valores_nos_slots[i]
        b = valores_nos_slots[i + 1]
        if a is None or b is None:
            continue
        if a in PROIBICOES and b in PROIBICOES[a]:
            valores_verificados1 = a
            valores_verificados2 = b
            print(f"PROIBIÇÃO ENCONTRADA: {a} ao lado de {b}")
            return True
    # nada encontrado -> limpar valores de verificação
    valores_verificados1 = None
    valores_verificados2 = None
    return False


def criar_nova_carta_aleatoria(todos_dados_cartas, x, y):
    """Escolhe um dado de carta aleatório e cria Carta. Retorna None se lista vazia."""
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
    """Retorna lista com 'quantidade' cartas posicionadas horizontalmente."""
    cartas = []
    for i in range(quantidade):
        x = x_mao + i * (largura_carta + espaco)
        c = criar_nova_carta_aleatoria(todos_dados_cartas, x, y_mao)
        if c:
            cartas.append(c)
    return cartas


# ----------------------------
# Tela de jogo (principal)
# ----------------------------
def tela_jogo(screen, estado_atual, nivel):
    TODOS_DADOS_CARTAS = carregar_dados_cartas()
    if not TODOS_DADOS_CARTAS:
        return "menu"

    TELA_LARGURA, TELA_ALTURA = screen.get_size()

    # Criar slots centralizados
    largura_total_slots = (LARGURA_CARTA * NUM_SLOTS) + (ESPACO_SLOTS * (NUM_SLOTS - 1))
    x_inicial = (TELA_LARGURA - largura_total_slots) // 2
    y_slots = TELA_ALTURA - 190

    SLOTS = [Slot(x_inicial + i * (LARGURA_CARTA + ESPACO_SLOTS), y_slots, LARGURA_CARTA, ALTURA_CARTA)
             for i in range(NUM_SLOTS)]

    # Cartas na mão (estado local da tela)
    cartas_na_mao = gerar_mao_aleatoria(TODOS_DADOS_CARTAS, LARGURA_CARTA, ESPACO_SLOTS)

    # Botões
    botao_novas_cartas = Botao(10, 10, 150, 40, "Cartas")
    x_finalizar = TELA_LARGURA - 160
    y_finalizar = y_slots - 60
    botao_finalizar = Botao(x_finalizar, y_finalizar, 150, 40, "Finalizar Rodada")

    # Estado de arraste / histórico
    carta_sendo_arrastada = None
    slot_original_da_carta = None
    lista_caixas_concluidas = []

    # Mensagem proibida
    tempo_fim_mensagem_proibida = 0

    fonte_nivel = criar_fonte(36)
    rodando_jogo = True

    # helpers para posicionamento consistente na mão
    def devolver_carta_para_mao(carta):
        """Adiciona carta ao final da lista de cartas_na_mao e a posiciona na próxima posição visível."""
        cartas_na_mao.append(carta)
        idx = len(cartas_na_mao) - 1
        carta.rect.topleft = (X_MAO + idx * (LARGURA_CARTA + ESPACO_SLOTS), Y_MAO)

    while rodando_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"

            # clique inicial
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if botao_novas_cartas.verificar_clique(event):
                    cartas_na_mao.clear()
                    cartas_na_mao.extend(gerar_mao_aleatoria(TODOS_DADOS_CARTAS, LARGURA_CARTA, ESPACO_SLOTS))
                    # reposicionar rects (garantir layout)
                    for i, c in enumerate(cartas_na_mao):
                        c.rect.topleft = (X_MAO + i * (LARGURA_CARTA + ESPACO_SLOTS), Y_MAO)

                # finalizar rodada
                slots_cheios = all(s.carta_colocada for s in SLOTS)
                if slots_cheios and botao_finalizar.verificar_clique(event):
                    if verificar_proibicao_adjacencia(SLOTS):
                        # caixa_mensagem pode retornar um timestamp ou não; lidamos com ambos os casos.
                        retorno = caixa_mensagem(
                            screen,
                            "Valores Proibidos Lado a Lado!",
                            TELA_LARGURA // 2,
                            TELA_ALTURA // 2,
                            2000
                        )
                        if isinstance(retorno, (int, float)):
                            tempo_fim_mensagem_proibida = retorno
                        else:
                            tempo_fim_mensagem_proibida = pygame.time.get_ticks() + 2000
                    else:
                        valores_slots = [s.carta_colocada.valor for s in SLOTS]
                        lista_caixas_concluidas.extend(valores_slots)
                        for s in SLOTS:
                            s.carta_colocada = None
                        return ('Pronto', nivel, lista_caixas_concluidas, 'menu')

                # iniciar drag (priorizar cartas na mão por cima)
                if not carta_sendo_arrastada:
                    for carta in reversed(cartas_na_mao):
                        if carta.iniciar_arrasto(mouse_pos):
                            carta_sendo_arrastada = carta
                            slot_original_da_carta = None
                            # trazer ao topo da renderização (remover/append)
                            cartas_na_mao.remove(carta)
                            cartas_na_mao.append(carta)
                            break

                    # se não achou na mão, checar slots
                    if not carta_sendo_arrastada:
                        for slot in SLOTS:
                            if slot.carta_colocada and slot.carta_colocada.iniciar_arrasto(mouse_pos):
                                carta_sendo_arrastada = slot.carta_colocada
                                slot_original_da_carta = slot
                                slot.carta_colocada = None
                                break

            # mover carta enquanto arrasta
            elif event.type == pygame.MOUSEMOTION:
                if carta_sendo_arrastada:
                    carta_sendo_arrastada.arrastar(event.pos)

            # soltar carta
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if carta_sendo_arrastada:
                    carta_sendo_arrastada.parar_arrasto()
                    soltou_no_slot = False

                    # tentar colocar na primeira slot que colidir
                    for slot in SLOTS:
                        if slot.rect.colliderect(carta_sendo_arrastada.rect):
                            if slot.carta_colocada is None:
                                slot.colocar_carta(carta_sendo_arrastada)
                                soltou_no_slot = True
                                # se veio da mão, já foi removida antes; se veio de slot, já foi removida também
                                break
                            else:
                                # swap entre carta arrastada e carta do slot
                                carta_do_slot = slot.remover_carta()
                                slot.colocar_carta(carta_sendo_arrastada)
                                soltou_no_slot = True
                                if slot_original_da_carta:
                                    # volta a carta removida para o slot original
                                    slot_original_da_carta.colocar_carta(carta_do_slot)
                                else:
                                    # carta veio da mão -> devolver para a mão de forma organizada
                                    devolver_carta_para_mao(carta_do_slot)
                                break

                    if not soltou_no_slot:
                        # se não soltou em slot, devolver para origem (slot ou mão)
                        if slot_original_da_carta:
                            slot_original_da_carta.colocar_carta(carta_sendo_arrastada)
                        else:
                            devolver_carta_para_mao(carta_sendo_arrastada)

                    carta_sendo_arrastada = None
                    slot_original_da_carta = None

        # --- desenho ---
        screen.fill((0, 0, 0))
        texto_nivel = fonte_nivel.render(f"NÍVEL: {nivel}", True, COR_BRANCO)
        screen.blit(texto_nivel, (TELA_LARGURA - texto_nivel.get_width() - 10, 10))

        for slot in SLOTS:
            slot.desenhar(screen)

        # desenhar cartas na mão (exceto a que está sendo arrastada)
        for carta in cartas_na_mao:
            if carta is not carta_sendo_arrastada:
                carta.desenhar(screen)

        botao_novas_cartas.desenhar(screen)

        if all(s.carta_colocada for s in SLOTS):
            botao_finalizar.desenhar(screen)

        if carta_sendo_arrastada:
            # desenhar por cima
            carta_sendo_arrastada.desenhar(screen)

        # mensagem proibida (se estiver ativa)
        if tempo_fim_mensagem_proibida > pygame.time.get_ticks():
            texto = "IMPOSSÍVEL JOGAR AQUI!"
            if valores_verificados1 is not None and valores_verificados2 is not None:
                texto = f"IMPOSSÍVEL JOGAR AQUI! {valores_verificados1} e {valores_verificados2} não podem estar juntos!"
            caixa_mensagem(screen, texto, TELA_LARGURA // 2, TELA_ALTURA // 2, 0)

        pygame.display.flip()
