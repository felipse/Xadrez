# Jogo de Xadrez em Pygame

## Descrição

Este é um jogo de xadrez simples implementado em Python utilizando a biblioteca Pygame. Ele apresenta uma interface gráfica para jogar xadrez, com todas as peças e regras básicas do jogo, incluindo roque e promoção de peões.

## Como Instalar/Configurar

1.  **Certifique-se de ter o Python instalado.** Você pode baixá-lo em [python.org](https://www.python.org/).
2.  **Instale a biblioteca Pygame.** Abra o terminal ou prompt de comando e execute:
    ```bash
    pip install pygame
    ```
3.  **Clone ou baixe este repositório.**
4.  **Navegue até o diretório do projeto** no seu terminal.

## Como Usar

Para iniciar o jogo, execute o seguinte comando no diretório do projeto:

```bash
python xadrez.py
```

O jogo abrirá em uma nova janela. As regras são as do xadrez padrão:
- Clique em uma peça para selecioná-la.
- Os movimentos válidos para a peça selecionada serão destacados.
- Clique em um dos quadrados destacados para mover a peça.
- O jogo alterna os turnos entre branco e preto.
- O jogo termina em xeque-mate ou empate por afogamento.

## Estrutura do Projeto

-   `xadrez.py`: Contém a lógica principal do jogo, incluindo a interface gráfica, o tabuleiro, as regras de movimento das peças e a detecção de fim de jogo.
-   `classes.py`: (Atualmente, este arquivo parece ser uma versão inicial ou um rascunho e não é totalmente utilizado pela lógica principal em `xadrez.py`. A definição das peças está majoritariamente dentro de `xadrez.py`).
-   `imagens/`: Contém as imagens das peças do xadrez (brancas e pretas).

## Como Contribuir

Contribuições são bem-vindas! Se você tiver ideias para melhorias, novas funcionalidades ou correções de bugs:

1.  Faça um fork do projeto.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/nova-feature`).
3.  Faça commit de suas mudanças (`git commit -am 'Adiciona nova feature'`).
4.  Faça push para a branch (`git push origin feature/nova-feature`).
5.  Abra um Pull Request.

## Licença

Este projeto é de código aberto. Sinta-se à vontade para usá-lo e modificá-lo. (Se desejar, adicione uma licença específica aqui, como MIT, GPL, etc.)
