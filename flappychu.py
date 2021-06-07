import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if pika_rect.colliderect(pipe):
            death_sound.play()
            return False

    if pika_rect.top <= -100 or pika_rect.bottom >= 900:
        return False

    return True

def rotate_pika(pika):
    new_pika = pygame.transform.rotozoom(pika,-pika_movement * 3,1)
    return new_pika

def pika_animation():
    new_pika = pika_frames[pika_index]
    new_pika_rect = new_pika.get_rect(center = (100, pika_rect.centery))
    return new_pika,new_pika_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score >high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.25
pika_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

pika_downflap = pygame.transform.scale2x(pygame.image.load('assets/pikachu-downflap.png').convert_alpha())
pika_midflap = pygame.transform.scale2x(pygame.image.load('assets/pikachu-midflap.png').convert_alpha())
pika_upflap = pygame.transform.scale2x(pygame.image.load('assets/pikachu-upflap.png').convert_alpha())
pika_frames = [pika_downflap,pika_midflap,pika_upflap]
pika_index = 0
pika_surface = pika_frames[pika_index]
pika_rect = pika_surface.get_rect(center = (100,512))

PIKAFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PIKAFLAP,200)


pipe_surface = pygame.image.load('assets/pipe.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                pika_movement = 0
                pika_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                pipe_list.clear()
                pika_rect.center = (100,512)
                pika_movement = 0
                score = 0


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == PIKAFLAP:
            if pika_index < 2:
                pika_index += 1
            else:
                pika_index = 0

            pika_surface,pika_rect = pika_animation()


    screen.blit(bg_surface,(0,0))

    if game_active:
        #Pika
        pika_movement += gravity
        rotated_pika = rotate_pika(pika_surface)
        pika_rect.centery += pika_movement
        screen.blit(rotated_pika,pika_rect)
        game_active = check_collision(pipe_list)

        #Pipes

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    #Floot
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos =0

    pygame.display.update()
    clock.tick(120)