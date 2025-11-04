# 🪄 Magos Malucos: O Desafio da Ordenação Mágica

![Carta de mago — Imagem de capa](Imagens/Arcano1.png)

Bem-vindo a **Magos Malucos**, um jogo desenvolvido em Pygame-CE que mistura estratégia de cartas com o desafio clássico de algoritmos de ordenação. Sua missão é organizar as cartas em seus slots inferiores em ordem crescente para acumular Experiência (XP) e subir de Nível!

## 🚀 Como Jogar

O objetivo principal do jogo é organizar as cartas nos **4 Slots** inferiores em **ordem crescente de seus valores** para maximizar seu XP a cada rodada.

### 🃏 A Tela de Jogo

| Área | Descrição |
| :--- | :--- |
| **Mão de Cartas** (Topo) | É onde suas cartas iniciais estão. Arraste as cartas daqui para os Slots. |
| **Slots** (Embaixo) | Quatro espaços vazios onde as cartas são colocadas. Sua ordem final aqui é o que será avaliado. |
| **Nível e XP** (Canto Superior) | Indica seu progresso atual. |
| **Botão `+ Cartas`** | Limpa sua mão e gera 4 novas cartas aleatórias. |
| **Botão `Finalizar Jogada`** | Inicia a avaliação da rodada. Só fica disponível quando todos os Slots estão preenchidos. |

### 🧠 Regras de Ação

1.  **Arraste e Solte (Drag & Drop):** Mova as cartas entre a Mão e os Slots.
2.  **Troca de Slots:** Arrastar uma carta para um Slot já ocupado fará com que as cartas troquem de lugar.
3.  **Devolver para a Mão:** Arrastar uma carta de um Slot e soltá-la em um lugar que **não seja outro Slot** fará com que ela retorne à sua Mão.

### 🛑 Regra de Proibição Mágica

Existe uma regra de adjacência mágica que você **DEVE** evitar:

* **Valores Proibidos:** Cartas com valores `[1, 2, 3, 7, 8, 9]` **não podem** ficar imediatamente ao lado de cartas com valores `[4, 5, 6, 10, 11, 12]`.

Se você tentar finalizar a jogada com uma proibição ativa, a jogada será cancelada, e você receberá uma mensagem de erro na tela.

### ⭐ Ganhando e Perdendo XP

Após apertar **Finalizar Jogada**, o jogo avalia se a ordem de suas cartas corresponde à ordem crescente correta.

| Resultado da Avaliação | Pontuação |
| :--- | :--- |
| ✅ **Posição Correta:** A carta está na **posição exata** que deveria estar na ordem crescente. | **+5 XP** |
| ❌ **Posição Incorreta:** A carta está em uma **posição diferente** da correta. | **-1 XP** |

Seu XP mínimo é 0.

### 📈 Nível e Progresso

* A cada **10 XP** acumulados, você sobe **1 Nível**.
* Ao subir de Nível, o XP é resetado, e o XP restante se torna seu novo XP base.
* **Nota:** Após finalizar a jogada, uma tela de processamento temporária aparecerá por 5 segundos, exibindo o resultado detalhado do cálculo de XP antes de retornar à tela de jogo.

## ⚙️ Configuração (Para Desenvolvedores)

### Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado.

### Instalação

1.  Clone o repositório:
    ```bash
    git clone [LINK_DO_SEU_REPOSITÓRIO]
    cd MagosMalucos
    ```
2.  Instale as dependências:
    ```bash
    pip install pygame-ce
    ```

### Execução

Para iniciar o jogo:
```bash
python Pygame_main.py