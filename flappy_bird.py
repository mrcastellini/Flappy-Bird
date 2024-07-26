import pygame
import random
import os

# Inicializar o Pygame
pygame.init()

# Inicializar o Pygame Mixer
pygame.mixer.init()

# Carregar e configurar o som do pulo
jump_sound = pygame.mixer.Sound(os.path.join('sons', 'jump_sound.mp3'))

# Carregar e configurar o som de Game Over
game_over_sound = pygame.mixer.Sound(os.path.join('sons', 'game_over.wav'))

# Definir as dimensões da tela
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Definir as cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
gray = (128, 128, 128)
light_gray = (200, 200, 200)
yellow_egg = (254, 203, 54)
yellow_nog = (241, 178, 16)

# Caminho para a fonte
font_path1 = os.path.join('fontes', 'Montserrat-Medium.ttf')
font_path2 = os.path.join('fontes', 'Montserrat-Bold.ttf')

# Carregar a fonte personalizada
font1 = pygame.font.Font(font_path1, 12)
font2 = pygame.font.Font(font_path2, 22)
font_game_over = pygame.font.Font(font_path2, 48)
font_try_again = pygame.font.Font(font_path1, 17)

# Carregar e redimensionar imagens
bird_flap_image = pygame.image.load(os.path.join('imagens', 'bird_flap.png'))
bird_flap_image = pygame.transform.scale(bird_flap_image, (50, 35))
bird_idle_image = pygame.image.load(os.path.join('imagens', 'bird_idle.png'))
bird_idle_image = pygame.transform.scale(bird_idle_image, (50, 35))
pipe_image = pygame.image.load(os.path.join('imagens', 'pipe.png'))
pipe_image = pygame.transform.scale(pipe_image, (78, 600))  # Ajustar o tamanho do cano conforme necessário
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)  # Criar a versão invertida do cano

# Carregar e redimensionar imagem de fundo
background_image = pygame.image.load(os.path.join('imagens', 'sky.jpg'))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Carregar e reproduzir a música de fundo
pygame.mixer.music.load(os.path.join('sons', 'theme_song.mp3'))  # Substitua pelo caminho para o seu arquivo de música
pygame.mixer.music.set_volume(0.5)  # Ajuste o volume conforme necessário (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop

# Definir a velocidade do jogo
clock = pygame.time.Clock()
fps = 30

# Definir a posição e a velocidade do pássaro
bird_x = 50
bird_y = 300
bird_velocity = 0
gravity = 0.5

# Definir a posição e a velocidade dos canos
pipe_width = 70
pipe_height_inst = 200
pipe_height = random.randint(150, 450)
pipe_x = screen_width
pipe_velocity = 3
pipe_gap = 150  # Adicione esta linha

# Definir a posição e a velocidade do fundo
background_x = 0
background_velocity = 1

# Variáveis para a distância percorrida e pontuação
distance_covered = 0
score = 0

# Função para desenhar o texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Função para desenhar um retângulo com efeito degradê e borda preta
def draw_gradient_rect(surface, rect, color1, color2, border_color, border_width):
    x, y, w, h = rect
    for i in range(h):
        r = color1[0] + (color2[0] - color1[0]) * i // h
        g = color1[1] + (color2[1] - color1[1]) * i // h
        b = color1[2] + (color2[2] - color1[2]) * i // h
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
    pygame.draw.rect(surface, border_color, rect, border_width)

# Função para exibir a tela de introdução
def show_instructions():
    instructions_running = True
    while instructions_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    instructions_running = False
                    
        # Desenhar o plano de fundo
        screen.fill(white)
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + screen_width, 0))
        screen.blit(bird_idle_image, (bird_x, bird_y))

        # Definir a posição e tamanho da caixa de texto
        textbox = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 100, 200, 50)
        
        # Definir nova largura e posição da caixa de texto
        textbox_width = 380
        textobox_height = 230
        textbox_x = screen_width / 2 - textbox_width / 2
        textbox_y = screen_height / 9
        
        # Criar a caixa de texto com as novas dimensões e posição
        textbox = pygame.Rect(textbox_x, textbox_y, textbox_width, textobox_height)
        button_color1 = white
        button_color2 = white
        draw_gradient_rect(screen, textbox, button_color1, button_color2, black, 3)
        
        # Desenhar a mensagem instruções
        draw_text("INSTRUÇÕES", font2, black, screen, screen_width / 2, screen_height / 2 - 200)
        
        # Definir as linhas de texto
        lines = [
            "Use a barra de espaço para controlar o pássaro.",
            "Evite os canos e tente voar o mais longe possível!",
            "Pressione a barra de espaço para começar."
        ]
        
        # Desenhar cada linha de texto
        for i, line in enumerate(lines):
            draw_text(line, font1, black, screen, screen_width / 2, screen_height / 2 - 130 + i * 30)
        
        pygame.display.update()
        clock.tick(fps)

# Função principal do jogo
def game_loop():
    global bird_y, bird_velocity, pipe_x, pipe_height, background_x, distance_covered, score
    
    game_over = False
    game_running = True
    bird_flap = True  # Estado inicial da animação
    flap_timer = 0  # Timer para controlar a animação
    
    # Definir a posição e tamanho do botão tentar novamente
    retry_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 100, 200, 50)
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        game_over = False
                        bird_y = 300
                        bird_velocity = 0
                        pipe_x = screen_width
                        pipe_height = random.randint(150, 450)
                        distance_covered = 0  # Resetar a distância ao reiniciar o jogo
                        score = 0  # Resetar a pontuação ao reiniciar o jogo
                    else:
                        bird_velocity = -8
                        jump_sound.play()  # Reproduzir o som do pulo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    mouse_x, mouse_y = event.pos
                    if retry_button.collidepoint(mouse_x, mouse_y):
                        game_over = False
                        bird_y = 300
                        bird_velocity = 0
                        pipe_x = screen_width
                        pipe_height = random.randint(150, 450)
                        distance_covered = 0  # Resetar a distância ao reiniciar o jogo
                        score = 0  # Resetar a pontuação ao reiniciar o jogo
        
        if not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity
            
            pipe_x -= pipe_velocity
            if pipe_x < -pipe_width:
                pipe_x = screen_width
                pipe_height = random.randint(150, 450)
                distance_covered += 1  # Aumenta a distância percorrida
                score += 1  # Incrementa a pontuação quando o pássaro passa por um cano
            
            background_x -= background_velocity
            if background_x <= -screen_width:
                background_x = 0
            
            if (bird_y > screen_height - bird_flap_image.get_height()) or (bird_y < 0):
                game_over = True
                game_over_sound.play()  # Reproduzir o som de Game Over ao detectar colisão
            
            if (pipe_x < bird_x < pipe_x + pipe_width or pipe_x < bird_x + bird_flap_image.get_width() < pipe_x + pipe_width):
                if not (pipe_height < bird_y < pipe_height + pipe_gap):
                    game_over = True
                    game_over_sound.play()  # Reproduzir o som de Game Over ao detectar colisão
            
            # Atualizar a animação do pássaro
            flap_timer += 1
            if flap_timer % 10 == 0:  # Alterne a imagem a cada 10 frames
                bird_flap = not bird_flap
            
        screen.fill(white)
        
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + screen_width, 0))
        
        if not game_over:
            # Usar a imagem de animação do pássaro
            if bird_flap:
                screen.blit(bird_flap_image, (bird_x, bird_y))
            else:
                screen.blit(bird_idle_image, (bird_x, bird_y))
            
            screen.blit(pipe_image, (pipe_x, pipe_height + pipe_gap))
            screen.blit(pipe_image_flipped, (pipe_x, pipe_height - pipe_image_flipped.get_height()))
            
            # Desenhar o contador de pontuação
            draw_text(f"Pontuação: {distance_covered}", font2, black, screen, 90, 30)
            
        else:
            # Esmaecer a imagem de fundo
            fade_surface = pygame.Surface((screen_width, screen_height))
            fade_surface.set_alpha(128)  # Ajuste o valor para o nível de esmaecimento (0-255)
            fade_surface.fill(black)
            screen.blit(fade_surface, (0, 0))
            
            # Desenhar a mensagem de fim de jogo
            draw_text("FIM DE JOGO", font_game_over, white, screen, screen_width / 2, screen_height / 2 - 100)
            
            # Desenhar a pontuação final
            draw_text(f"Sua pontuação foi de: {score}", font2, white, screen, screen_width / 2, screen_height / 2 + 10)
            
            # Desenhar o botão de tentar novamente
            mouse_pos = pygame.mouse.get_pos()
            if retry_button.collidepoint(mouse_pos):
                button_color1 = yellow_nog
                button_color2 = yellow_nog
            else:
                button_color1 = yellow_egg
                button_color2 = yellow_egg
        
            draw_gradient_rect(screen, retry_button, button_color1, button_color2, black, 3)
            
            draw_text("TENTAR NOVAMENTE", font_try_again, black, screen, screen_width / 2, screen_height / 2 + 125)
        
        pygame.display.update()
        clock.tick(fps)

    pygame.mixer.music.stop()  # Parar a música de fundo
    
    pygame.quit()

# Mostrar a tela de instruções antes de iniciar o jogo
show_instructions()
game_loop()
