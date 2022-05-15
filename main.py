import random
import sys
import pygame


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    new_pipe = surface_list.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = surface_list.get_rect(midbottom=(700, random_pipe_pos - 270))
    return new_pipe, top_pipe


# pipes speed
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(surface_list, pipe)
        else:
            flip_pipe = pygame.transform.flip(surface_list, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = random.choice(colour_bird)
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
        sound_point.play()
    return high_score


pygame.init()

screen = pygame.display.set_mode((288, 512))

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 30)

# game x
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
sound_die = pygame.mixer.Sound('hehe/sound/sfx_die.wav')
sound_point = pygame.mixer.Sound('hehe/sound/sfx_point.wav')
sound_wing = pygame.mixer.Sound('hehe/sound/sfx_wing.wav')
#
bg_surface1 = pygame.image.load('hehe/assets/background-day.png').convert_alpha()
bg_surface1 = pygame.transform.scale2x(bg_surface1)
bg_surface2 = pygame.image.load('hehe/assets/background-night.png').convert_alpha()
bg_surface2 = pygame.transform.scale2x(bg_surface2)
bg_list = random.choice([bg_surface1, bg_surface2])
bg_lsurface = bg_list.get_rect(center=(144, 190))

floor_surface = pygame.image.load('hehe/assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0


bird_blue_downflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/bluebird-downflap.png').convert_alpha())
bird_blue_midflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/bluebird-midflap.png').convert_alpha())
bird_blue_upflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/bluebird-upflap.png').convert_alpha())
bluebird_frames = [bird_blue_downflap, bird_blue_midflap, bird_blue_upflap]
bird_index = 0
bird_surface = bluebird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

bird_red_downflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/redbird-downflap.png').convert_alpha())
bird_red_midflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/redbird-midflap.png').convert_alpha())
bird_red_upflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/redbird-upflap.png').convert_alpha())
redbird_frames = [bird_red_downflap, bird_red_midflap, bird_red_upflap]
redbird_index = 0
redbird_surface = redbird_frames[redbird_index]
redbird_rect = redbird_surface.get_rect(center=(100, 512))

bird_yellow_downflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/yellowbird-downflap.png').convert_alpha())
bird_yellow_midflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/yellowbird-midflap.png').convert_alpha())
bird_yellow_upflap = pygame.transform.scale2x(pygame.image.load('hehe/assets/yellowbird-upflap.png').convert_alpha())
yellowbird_frames = [bird_yellow_downflap, bird_yellow_midflap, bird_yellow_upflap]
yellowbird_index = 0
yellowbird_surface = yellowbird_frames[yellowbird_index]
yellowbird_rect = redbird_surface.get_rect(center=(100, 512))

colour_bird = bluebird_frames[bird_index], redbird_frames[redbird_index], yellowbird_frames[yellowbird_index]

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

greenpipe_surface = pygame.image.load('hehe/assets/pipe-green.png')
greenpipe_surface = pygame.transform.scale2x(greenpipe_surface)
redpipe_surface = pygame.image.load('hehe/assets/pipe-red.png')
redpipe_surface = pygame.transform.scale2x(redpipe_surface)
surface_list = random.choice([greenpipe_surface, redpipe_surface])
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 600)
pipe_height = [200, 300, 400]

# game cycle
while True:
    # events cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                sound_wing.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                sound_die.play()
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # back pic
    screen.blit(bg_list, bg_lsurface)

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
        gameover_surface = game_font.render(f'GAME OVER', True, (255, 0, 0))
        gameover_rect = gameover_surface.get_rect(center=(144, 240))
        screen.blit(gameover_surface, gameover_rect)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
