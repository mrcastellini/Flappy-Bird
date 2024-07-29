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

# Variáveis para armazenar o nome do jogador e as pontuações
player_name = ''
scores = []

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

# Função para exibir a tela de instrução
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

# Função para exibir a tela de entrada do nome
def show_name_entry(max_length=7):
    global player_name
    input_active = True
    player_name = ''
    input_box = pygame.Rect(screen_width / 2 - 100, screen_height / 4, 150, 50)
    color_inactive = pygame.Color('black')  # Cor da borda da caixa de texto
    color_active = pygame.Color('dodgerblue2')
    color_box = pygame.Color('gray')  # Cor de fundo da caixa de texto
    color = color_inactive
    font = font2
    txt_surface = font.render(player_name, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < max_length:  # Verifica se o comprimento do nome é menor que o máximo
                    player_name += event.unicode
                txt_surface = font.render(player_name, True, color)
                input_box.w = max(200, txt_surface.get_width() + 10)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not input_active:
                    return

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

        # Desenhar a mensagem de entrada
        draw_text("Digite seu nome:", font2, black, screen, screen_width / 2, screen_height / 4 - 50)
        draw_text("Pressione ENTER para continuar", font1, black, screen, screen_width / 2, screen_height / 2 - 50)

        # Desenhar a caixa de texto com fundo branco e borda preta
        pygame.draw.rect(screen, color_box, input_box)
        pygame.draw.rect(screen, color_inactive, input_box, 2)  # Borda preta

        # Centralizar o texto na caixa de entrada
        txt_surface = font.render(player_name, True, color)
        txt_rect = txt_surface.get_rect(center=input_box.center)
        screen.blit(txt_surface, txt_rect)

        pygame.display.update()
        clock.tick(fps)

# Função para salvar a pontuação em um arquivo de texto, garantindo que cada pontuação seja armazenada apenas uma vez
def save_score(player_name, score):
    file_path = 'scores.txt'
    
    # Ler o conteúdo existente
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    
    # Criar um dicionário para armazenar as pontuações
    scores_dict = {}
    for line in lines:
        name, high_score_str = line.split(':')
        high_score = int(high_score_str.strip())
        scores_dict[name] = high_score
    
    # Atualizar a maior pontuação ou adicionar nova entrada
    if player_name in scores_dict:
        scores_dict[player_name] = max(scores_dict[player_name], score)
    else:
        scores_dict[player_name] = score
    
    # Escrever o novo conteúdo no arquivo
    with open(file_path, 'w') as file:
        for name, high_score in scores_dict.items():
            file.write(f"{name}: {high_score}\n")

# Função para exibir as pontuações dos jogadores
def show_high_scores():
    file_path = 'scores.txt'
    
    # Ler o conteúdo existente
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    
    # Criar uma lista para armazenar as pontuações
    scores_list = []
    for line in lines:
        name, high_score_str = line.split(':')
        high_score = int(high_score_str.strip())
        scores_list.append((name, high_score))
    
    # Ordenar as pontuações em ordem decrescente
    scores_list.sort(key=lambda x: x[1], reverse=True)

    # Selecionar as 10 melhores pontuações
    top_10_scores = scores_list[:10]
    
    # Exibir as pontuações na tela
    display_scores = True
    while display_scores:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    display_scores = False
        
        screen.fill(white)
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + screen_width, 0))

        # Definir a posição e tamanho da caixa de texto
        textbox = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 100, 200, 50)
        
        # Definir nova largura e posição da caixa de texto
        textbox_width = 380
        textobox_height = 450
        textbox_x = screen_width / 2 - textbox_width / 2
        textbox_y = screen_height / 9
        
        # Criar a caixa de texto com as novas dimensões e posição
        textbox = pygame.Rect(textbox_x, textbox_y, textbox_width, textobox_height)
        button_color1 = white
        button_color2 = white
        draw_gradient_rect(screen, textbox, button_color1, button_color2, black, 3)
        
        # Desenhar a mensagem de pontuações
        draw_text("RANKING", font_game_over, black, screen, screen_width / 2, screen_height / 2 - 200)
        
        # Desenhar as pontuações
        for i, (name, score) in enumerate(top_10_scores):
            draw_text(f"{i + 1}. {name}: {score}", font2, black, screen, screen_width / 2, screen_height / 2 - 130 + i * 30)
        
        draw_text("Pressione a barra de espaço para voltar", font1, black, screen, screen_width / 2, screen_height / 2 + 185)
        
        pygame.display.update()
        clock.tick(fps)

# Função principal do jogo
def game_loop():
    global bird_y, bird_velocity, pipe_x, pipe_height, background_x, distance_covered, score, player_name
    global pipe_velocity, background_velocity

    game_over = False
    game_running = True
    bird_flap = True  # Estado inicial da animação
    flap_timer = 0  # Timer para controlar a animação
    pipes_passed = 0  # Variável para contar quantos canos foram passados
    generate_sequential_pipes = False  # Flag para indicar se canos sequenciais devem ser gerados
    sequential_pipe_count = 0  # Contador para canos sequenciais
    sequential_pipe_x_positions = []  # Lista para armazenar as posições x dos canos sequenciais
    sequential_pipe_heights = []  # Lista para armazenar as alturas dos canos sequenciais
    generate_standard_pipes = True  # Flag para controlar a geração de canos padrão
    score = 0  # Inicializa a pontuação com 0
    score_reached_20 = False  # Flag para indicar se a pontuação atingiu 20

    # Definir a posição e tamanho dos botões
    retry_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 100, 200, 50)
    ranking_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 170, 200, 50)

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
                        distance_covered = 0
                        score = 0
                        pipes_passed = 0
                        pipe_velocity = 3
                        background_velocity = 1
                        generate_sequential_pipes = False
                        sequential_pipe_count = 0
                        sequential_pipe_x_positions = []
                        sequential_pipe_heights = []
                        generate_standard_pipes = True  # Reiniciar a geração de canos padrão
                        score_reached_20 = False  # Resetar a flag
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
                        distance_covered = 0
                        score = 0
                        pipes_passed = 0
                        pipe_velocity = 3
                        background_velocity = 1
                        generate_sequential_pipes = False
                        sequential_pipe_count = 0
                        sequential_pipe_x_positions = []
                        sequential_pipe_heights = []
                        generate_standard_pipes = True  # Reiniciar a geração de canos padrão
                        score_reached_20 = False  # Resetar a flag
                    elif ranking_button.collidepoint(mouse_x, mouse_y):
                        show_high_scores()

        if not game_over:
            bird_velocity += gravity
            bird_y += bird_velocity

            if generate_sequential_pipes:
                for idx, sp_x in enumerate(sequential_pipe_x_positions):
                    sequential_pipe_x_positions[idx] -= pipe_velocity
                    if sp_x < -pipe_width:
                        sequential_pipe_x_positions.pop(idx)
                        sequential_pipe_heights.pop(idx)
                        sequential_pipe_count -= 1
                        distance_covered += 1
                        score += 1
                        pipes_passed += 1

                        if sequential_pipe_count == 0:
                            generate_sequential_pipes = False
                            generate_standard_pipes = score < 20  # Permitir a geração de canos padrão apenas se a pontuação for menor que 20

                    if pipes_passed % 10 == 0:
                        pipe_velocity += 0.001
                        background_velocity += 0.001

            if generate_standard_pipes:
                pipe_x -= pipe_velocity
                if pipe_x < -pipe_width:
                    pipe_x = screen_width
                    pipe_height = random.randint(150, 450)
                    distance_covered += 1
                    score += 1
                    pipes_passed += 1

                    if pipes_passed % 10 == 0:
                        pipe_velocity += 1
                        background_velocity += 0.5

                    if pipes_passed >= 20:
                        score_reached_20 = True


            if score_reached_20 and not generate_sequential_pipes and sequential_pipe_count == 0:
                generate_sequential_pipes = True
                sequential_pipe_count = 3
                sequential_pipe_x_positions = []
                sequential_pipe_heights = [random.randint(150, 450) for _ in range(sequential_pipe_count)]


                for i in range(sequential_pipe_count):
                    sequential_pipe_x_positions.append(screen_width + i * (pipe_width + 150))
                generate_standard_pipes = False  # Impedir a geração de canos padrão

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

            for idx, sp_x in enumerate(sequential_pipe_x_positions):
                if (sp_x < bird_x < sp_x + pipe_width or sp_x < bird_x + bird_flap_image.get_width() < sp_x + pipe_width):
                    if not (sequential_pipe_heights[idx] < bird_y < sequential_pipe_heights[idx] + pipe_gap):
                        game_over = True
                        game_over_sound.play()  # Reproduzir o som de Game Over ao detectar colisão

            flap_timer += 1
            if flap_timer % 10 == 0:  # Alterne a imagem a cada 10 frames
                bird_flap = not bird_flap

        screen.fill(white)

        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + screen_width, 0))

        if not game_over:
            if bird_flap:
                screen.blit(bird_flap_image, (bird_x, bird_y))
            else:
                screen.blit(bird_idle_image, (bird_x, bird_y))

            if generate_standard_pipes:
                screen.blit(pipe_image, (pipe_x, pipe_height + pipe_gap))
                screen.blit(pipe_image_flipped, (pipe_x, pipe_height - pipe_image_flipped.get_height()))

            if generate_sequential_pipes:
                for idx, sp_x in enumerate(sequential_pipe_x_positions):
                    screen.blit(pipe_image, (sp_x, sequential_pipe_heights[idx] + pipe_gap))
                    screen.blit(pipe_image_flipped, (sp_x, sequential_pipe_heights[idx] - pipe_image_flipped.get_height()))

            draw_text(f"Pontuação: {distance_covered}", font2, black, screen, 90, 30)

        else:
            fade_surface = pygame.Surface((screen_width, screen_height))
            fade_surface.set_alpha(128)
            fade_surface.fill(black)
            screen.blit(fade_surface, (0, 0))

            draw_text("FIM DE JOGO", font_game_over, white, screen, screen_width / 2, screen_height / 2 - 100)
            draw_text(f"Sua pontuação foi de: {score}", font2, white, screen, screen_width / 2, screen_height / 2 + 10)

            scores.append((player_name, score))
            save_score(player_name, score)

            mouse_pos = pygame.mouse.get_pos()
            if retry_button.collidepoint(mouse_pos):
                button_color1 = yellow_nog
                button_color2 = yellow_nog
            else:
                button_color1 = yellow_egg
                button_color2 = yellow_egg

            draw_gradient_rect(screen, retry_button, button_color1, button_color2, black, 3)
            draw_text("TENTAR NOVAMENTE", font_try_again, black, screen, screen_width / 2, screen_height / 2 + 125)

            # Desenhar o botão de ranking
            if ranking_button.collidepoint(mouse_pos):
                button_color1 = yellow_nog
                button_color2 = yellow_nog
            else:
                button_color1 = yellow_egg
                button_color2 = yellow_egg

            draw_gradient_rect(screen, ranking_button, button_color1, button_color2, black, 3)
            draw_text("RANKING", font_try_again, black, screen, screen_width / 2, screen_height / 2 + 195)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Mostrar a tela de instruções antes de iniciar o jogo
show_instructions()

# Mostrar a tela de entrada do nome antes de iniciar o jogo
show_name_entry()

# Iniciar o loop do jogo
game_loop()
