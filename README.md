***

# 🧙‍♂️ MaGos MALucos 🃏

## Quebra-Cabeça de Cartas com Regras de Adjacência

**MaGos MALucos** é um jogo de lógica e quebra-cabeça desenvolvido em Python utilizando a biblioteca Pygame.

O objetivo principal é preencher os **4 Slots** disponíveis com cartas da sua mão, garantindo que as rigorosas regras de proibição de adjacência (vizinhos) sejam respeitadas. Ao encontrar um arranjo válido, o jogador clica em "Finalizar Rodada" para avançar.

***

## 🌟 Regra Principal: A Proibição Mágica

A lógica central do jogo reside na função `verificar_proibicao_adjacencia` (presente em `jogo.py`), que impõe uma única regra:

**Nenhuma carta do Grupo 1 pode estar imediatamente ao lado (adjacente) de uma carta do Grupo 2.**

### Divisão dos Elementos

As cartas são categorizadas por seus valores numéricos (de 1 a 15):

* **Grupo 1 (Permissivos):** Valores $1, 2, 3$ (Fogo), $7, 8, 9$ (Terra), $13, 14, 15$ (Arcano). Estes podem ser vizinhos uns dos outros, mas **não** do Grupo 2.
* **Grupo 2 (Proibitivos):** Valores $4, 5, 6$ (Gelo), $10, 11, 12$ (Trevas). Estes podem ser vizinhos uns dos outros, mas **não** do Grupo 1.

> ❌ **Exemplo Proibido:** Fogo (Valor 1) $\leftrightarrow$ Gelo (Valor 4)
>
> ✅ **Exemplo Permitido:** Arcano (Valor 13) $\leftrightarrow$ Terra (Valor 7)

***

## 🎮 Como Jogar (Mecânicas)

1.  **Início:** Pressione **ESPAÇO** na tela de menu.
2.  **Mover:** Use o mouse para **arrastar e soltar** as cartas da sua Mão para um dos 4 Slots na parte inferior da tela.
3.  **Trocar:** Se um Slot já estiver ocupado, o ato de arrastar uma nova carta para ele **troca a posição** das duas cartas.
4.  **Nova Mão:** Use o botão "Cartas" para renovar sua mão com 4 cartas aleatórias.
5.  **Validação:** Clique em **"Finalizar Rodada"** após preencher todos os 4 Slots. O jogo notificará se houver uma quebra de regra.

***

## ⚙️ Estrutura Detalhada do Código

O projeto é modular, permitindo que cada arquivo Pygame lide com uma responsabilidade específica, facilitando a organização.

### 1. Núcleo e Fluxo do Jogo

* **`Pygame_main.py`**:
    * É o **ponto de entrada** e o loop principal do jogo.
    * Gerencia a transição de estados (`menu`, `jogo`, `ordenacao`).
* **`jogo.py`**:
    * Contém o *game loop* do nível ativo.
    * Implementa toda a lógica de interação (clique, arrasto e soltura de cartas).
    * Define as constantes **`LISTA_VALORES_PROIBIDOS_1/2`** e a função de validação **`verificar_proibicao_adjacencia`**.
* **`tela_menu.py`**:
    * Responsável por desenhar a tela inicial, incluindo o título "MaGos MALucos".
* **`ordenacao.py`**:
    * Módulo destinado a simular o **processamento pós-rodada** (`processar_ordenacao`), preparando os dados para o próximo nível.

### 2. Componentes e Dados

* **`cartas.py`**:
    * Define a classe fundamental **`Carta`**, que lida com a imagem, valor, nome e a mecânica de arrasto no Pygame.
* **`cartas.json`**:
    * O arquivo de dados essencial que armazena a lista estática de todas as cartas, mapeando o `nome` e `caminho_imagem` para o **`valor` numérico**.
* **`Slots.py`**:
    * Define a classe **`Slot`**, que representa o espaço onde as cartas devem ser posicionadas, gerenciando a sua visualização e posicionamento na tela.
* **`interface.py`**:
    * Módulo de utilitários de UI, definindo a **`class Botao`** e a função **`caixa_mensagem`** para notificações de erro.

### 3. Utilitários (Expansão e Suporte)

* **`ValidarImagem.py`**: Contém funções como `iniciar_geracao_e_validar`, sugerindo um sistema para lidar com o carregamento, redimensionamento ou, possivelmente, a geração de ativos gráficos dinamicamente.
* **`InputBox.py`**: Utilitário que define a `class InputBox` para capturar entrada de texto (não usada no *game loop* principal, mas pronta para debug ou futuros campos de nome/configuração).

***
