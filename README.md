# 🃏 Card Blocker

Um jogo de cartas em Pygame onde o desafio é preencher a linha de slots sem colocar cartas com valores proibidos lado a lado.

## ✨ Visão Geral do Jogo

O objetivo principal é completar a **linha de slots** com cartas da sua **mão**, respeitando a regra de que certos pares de valores de cartas não podem ser adjacentes. Ao preencher todos os slots sem violações, você completa a rodada e avança no jogo!

---

## 🎲 Como Jogar

### O Jogo Principal

1.  **Sua Mão:** No topo da tela, você tem uma **Mão** de cartas.
2.  **Slots:** Na parte inferior, há uma linha de **Slots** vazios (espaços para cartas).
3.  **Mecânica:** Use o mouse para **arrastar** as cartas da sua Mão para os Slots.
4.  **Movimentação:**
    * Você pode mover cartas da Mão para um Slot vazio.
    * Você pode mover cartas de um Slot para outro Slot vazio.
    * Você pode **trocar** uma carta arrastada por uma carta já presente em um Slot.
    * Se você soltar a carta fora de um Slot, ela volta para sua posição de origem (Mão ou Slot anterior).

### A Regra de Proibição de Adjacência (O Desafio)

O núcleo do jogo é a regra que impede que certos valores de cartas fiquem lado a lado.

| Grupo de Valores (A) | Valores Proibidos Adjacentes (B) |
| :------------------: | :------------------------------: |
| $\{1, 2, 3, 7, 8, 9\}$ | $\{4, 5, 6, 10, 11, 12\}$ |
| $\{4, 5, 6, 10, 11, 12\}$ | $\{1, 2, 3, 7, 8, 9\}$ |

> **Exemplo:** Se uma carta com valor `2` (Grupo A) estiver em um Slot, os Slots vizinhos (adjacentes) **não podem** conter cartas com valores do Grupo B (como `4` ou `10`).

### Finalizando a Rodada

* O botão **"Finalizar Rodada"** só estará ativo quando **todos os Slots estiverem preenchidos**.
* **Vitória:** Se você clicar em "Finalizar Rodada" e não houver nenhuma proibição de adjacência, você avança no jogo.
* **Derrota/Aviso:** Se você clicar em "Finalizar Rodada" e houver uma violação, uma **mensagem de erro** será exibida (ex: *"IMPOSSÍVEL JOGAR AQUI! 2 e 4 não podem estar juntos!"*). Você deve reposicionar as cartas para resolver a proibição.

### Botões de Controle

| Botão | Ação |
| :---: | :--- |
| **Cartas** | Descarta as cartas atuais da Mão e gera uma **nova Mão** aleatória (as cartas nos Slots não são afetadas). |
| **Finalizar Rodada** | Verifica a regra de proibição e finaliza a rodada (só ativo com todos os Slots preenchidos). |

---

## 🛠️ Instalação e Execução

### Pré-requisitos

Certifique-se de ter o Python e o Pygame instalados:

```bash
pip install pygame