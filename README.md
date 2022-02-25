# SpaceCrypto And Bombcrypto Bot - MultiScreen
This is a open source project inspired on bombcrypto-bot that was a success auto click bot that helped me a lot.

So, I decided to create a new auto click bot for the new NFT game space crypto. (It is not soo easy) I hope you like

To maintain the improvments and this auto click bot free, please help me with any value, have fun :)

Metamask wallet (BNB/SPG/BUSD/BCOIN): 0xa5e1412B4dBf4bE9Fb3f52b12aBFF7A78272B9b3

## Want bot for some game? enter discord and put which game!

## Quer bot para algum jogo? entra no discord e coloque qual jogo!

CANAL DISCORD
https://discord.gg/4gMA5Nhxrb

## Funções extras adicionadas

- Suporte a multiplas contas no mesmo monitor
- Todas funções para o bombcrypto
###### SpaceCrypto
- Fazer login.
- Refresh ao encontrar a mensagem de error
- Colocar naves para trabalhar
- Fazer surrender no boss que desejar.

Resolução: 1920x1080 e 1600x900

1920x1080 precisa está com escala 100%

1600x900 precisa está com escala 150%


Não pode ter Pasta ou Qualquer coisa que nao seja os jogos, nome com BombCrypto ou SpaceCrypto.


space:
  ###### ###PT### Tempo para colocar as naves para trabalhar
  ###### ###EN### Time to put the ships to work
  refresh_ships: 35
  ###### Surrender 3 to 12 need alter Images.
  ###### Default 0, Won't surrender.
  surrender_boss: 8
  ###### Add ships 100% = True.
  fight_100: True

# Instalação:

1- Baixe e instale Python na versão maior que 3 no [site oficial](https://www.python.org/downloads/) ou através da [windows store](https://www.microsoft.com/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab).

2 - Após instalado python:

- Para `windows` _execute como administrador_ o arquivo `run.bat` na pasta principal.
- Para `linux` o arquivo `run.sh` na pasta principal.

# Configurações:

Você pode configurar algumas opções alterando o arquivo `config.yaml` na pasta principal do bot.

## `scale_image`

- Você agora tem suporte de colocar quantos % de zoom está usando em seu navegador.

  > Se atente também ao ZOOM da janela de notificação do _Metamask_, ela deve ser a mesma usada no navegador.

  - ### `enable`

    Quando `True`, ativa a funcionalidade de usar um scale diferente. Caso contrário, deixe o valor como `False`

    > O valor deve ser: `True` ou `False`

  - ### `percent`
    A porcentagem de zoom do seu navegador e da janela de notificação do metamask.
    > O Valor deve ser de: `50` a `100`. Quanto menor o valor, mais impreciso serão as detecções do bot.

## `is_retina_screen`

- Caso seu computador seja um dispositivo mac com tela retina, será necessário ativar essa opção para que o bot realize clicks com precisão. Se seu bot move o mouse para lugares aleatórios, talvez essa opção te ajude.
  > O valor deve ser: `True` para ativar, ou `False` para desativar

## `mouse_move_speed`

- Você pode configurar a velocidade com que o mouse se move na tela antes da realização do click.
  > O valor deve ser de: `0.1` a `1`



# How to works?
The bot doesn't change any of the game's source code, it just takes a screenshot of the game's screen to find the buttons and simulates mouse movements.

#  Adjusting the bot

**Why some adjustments might be necessary?**

The bot uses image recognition to make decisions and move the mouse and click in the right places.
It accomplishes this by comparing an example image with a screenshot of the computer/laptop screen.
This method is subject to inconsistencies due to differences in your screen resolution and how the game is rendered on your computer.
It's likely that the bot doesn't work 100% on the first run, and you need to make some adjustments to the config file.

# Image Replacement
The images were taken on my computer with a resolution of 1920x1080. To replace an image that is not being recognized correctly, just find the corresponding image in the "targets" folder for BombCrypto and "img_compare" for SpaceCrypto, take a screenshot of the same area and replace the previous image. It is important that the replacement has the same name, including the .png extension.
