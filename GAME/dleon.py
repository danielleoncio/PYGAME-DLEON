import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

# Música de fundo
pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('Digimon.mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('smw_coin.wav')

# Configurações da tela e cores
largura = 640
altura = 480
AZUL = (0, 0, 80)

# Configurações da cobra
x_cobra = int(largura / 2)
y_cobra = int(altura / 2)
velocidade = 10  # velocidade inicial da cobra
x_controle = velocidade
y_controle = 0

# Posição da maçã
x_maca = randint(40, 600)
y_maca = randint(50, 430)

# Variáveis de jogo
pontos = 0
fonte = pygame.font.SysFont('bahnschrift', 25, False, False)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('JOGO DLEON')
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False

# Carregar todos os sprites para a animação de fundo
sprites_fundo = [
    pygame.image.load('IMG-20241105-WA0013.jpg'),
    pygame.image.load('IMG-20241105-WA0014.jpg'),
    pygame.image.load('IMG-20241105-WA0015.jpg'),
    pygame.image.load('IMG-20241105-WA0016.jpg'),
    pygame.image.load('IMG-20241105-WA0017.jpg'),
    pygame.image.load('IMG-20241105-WA0018.jpg'),
    pygame.image.load('IMG-20241105-WA0019.jpg'),
    pygame.image.load('IMG-20241105-WA0020.jpg')
]

# Redimensionar os sprites para caber na tela
sprites_fundo = [pygame.transform.scale(sprite, (largura, altura)) for sprite in sprites_fundo]

indice_sprite = 0  # Índice atual do sprite para a animação
tempo_animacao = 0  # Controlar o tempo de troca do sprite

# Função para aumentar a cobra
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.circle(tela, (0, 255, 0), (XeY[0], XeY[1]), 10)

# Função para reiniciar o jogo
def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu, indice_sprite, velocidade
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False
    indice_sprite = 0
    velocidade = 10  # Resetar a velocidade para o valor inicial

# Loop principal do jogo
while True:
    relogio.tick(30)
    
    # Atualizar o fundo da tela com o próximo sprite
    tela.blit(sprites_fundo[indice_sprite], (0, 0))
    tempo_animacao += 1
    if tempo_animacao > 5:  # Mudar de sprite a cada 5 frames
        indice_sprite = (indice_sprite + 1) % len(sprites_fundo)
        tempo_animacao = 0

    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))

    # Aumentar a velocidade conforme os pontos
    if pontos > 5 and pontos <= 10:
        velocidade = 12
    elif pontos > 10 and pontos <= 20:
        velocidade = 15
    elif pontos > 20:
        velocidade = 18

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_a and x_controle != velocidade:
                x_controle = -velocidade
                y_controle = 0
            if event.key == K_d and x_controle != -velocidade:
                x_controle = velocidade
                y_controle = 0
            if event.key == K_w and y_controle != velocidade:
                y_controle = -velocidade
                x_controle = 0
            if event.key == K_s and y_controle != -velocidade:
                y_controle = velocidade
                x_controle = 0

    x_cobra += x_controle
    y_cobra += y_controle

    # Desenhar a cobra e a maçã
    cobra = pygame.draw.circle(tela, (0, 255, 0), (x_cobra, y_cobra), 10)
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    # Verificar colisão com a maçã
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        barulho_colisao.play()
        comprimento_inicial += 1

    lista_cabeca = [x_cobra, y_cobra]
    lista_cobra.append(lista_cabeca)

    # Verificar colisão da cobra com ela mesma
    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('bahnschrift', 20, True, True)
        mensagem = 'Game over! Você se bateu. Pressione R para reiniciar.'
        texto_formatado = fonte2.render(mensagem, True, (238, 173, 45))
        ret_texto = texto_formatado.get_rect()
        morreu = True
        while morreu:
            tela.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    reiniciar_jogo()

            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    # Verificar se a cobra saiu da tela (morte)
    if x_cobra < 0 or x_cobra > largura or y_cobra < 0 or y_cobra > altura:
        fonte2 = pygame.font.SysFont('bahnschrift', 20, True, True)
        mensagem = 'Game over! Você bateu na borda. PRESS R'
        texto_formatado = fonte2.render(mensagem, True, (238, 173, 45))
        ret_texto = texto_formatado.get_rect()
        morreu = True
        while morreu:
            tela.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    reiniciar_jogo()

            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    # Limitar o crescimento da cobra
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)
    tela.blit(texto_formatado, (450, 40))

    pygame.display.update()
