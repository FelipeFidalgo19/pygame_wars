import random
import sys
from button import Button
import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projeto Computação Grafica!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (139, 0, 139)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 2, 0, 1, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/fire_gun.mp3')
WIN_SOUND = pygame.mixer.Sound('Assets/win.mp3')
MUSIC_SOUND = pygame.mixer.Sound('Assets/music.mp3')



HEALTH_FONT = pygame.font.SysFont('roboto', 40)
WINNER_FONT = pygame.font.SysFont('roboto', 100)
DAMEGE_FONT = pygame.font.SysFont('roboto', 20)

Damage = random.randint(5,50)
FPS = 60
VEL = 9
BULLET_VEL = 15
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


SPACE_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, MAGENTA, BORDER)

    damage_text = DAMEGE_FONT.render("PODER DE FOGO: " + str(Damage), 1, YELLOW)
    QUIT = DAMEGE_FONT.render("SAIR ", 1, WHITE)

    red_health_text = HEALTH_FONT.render(
        "INTEGRIDADE: " + str(red_health) + "%", 1, MAGENTA)
    yellow_health_text = HEALTH_FONT.render(
        "INTEGRIDADE: " + str(yellow_health) + "%", 1, MAGENTA)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(damage_text, (WIDTH - damage_text.get_width() - 10, 80))
    WIN.blit(QUIT, (10, 80))


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def press_mouse(mouse_pressed, mouse_pos, red, yellow, Damage):
    if mouse_pressed == (True, False, False):
        if mouse_pos[0] >= red.x and mouse_pos[0] <= red.x+50 and mouse_pos[1] >= red.y and mouse_pos[1] <= red.y+50:
            print("Clicado Vermelhor")
            pygame.display.update()
            main_menu()

        if mouse_pos[0] >= yellow.x and mouse_pos[0] <= yellow.x + 50 and mouse_pos[1] >= yellow.y and mouse_pos[1] <= yellow.y + 50:
            print("Clicado Amarelo")



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    WIN_SOUND.play()
    MUSIC_SOUND.stop()
    pygame.time.delay(7000)
    WIN_SOUND.stop()

def draw_menu(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(7000)

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def main():
    if MUSIC_SOUND.play() == False:
        MUSIC_SOUND.play()

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 100
    yellow_health = 100


    clock = pygame.time.Clock()
    run = True


    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_p and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= Damage
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= Damage
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Amarelo venceu!"

        if yellow_health <= 0:
            winner_text = "Vermelhor venceu!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        press_mouse(mouse_pressed, mouse_pos, red, yellow, Damage)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    # [loc, velocity, timer]
    particles = []
    while True:
        WIN.blit(SPACE_BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("NERD BATTLE", True, MAGENTA)
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(450, 250),
                             text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(450, 400),
                             text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)


        mx, my = pygame.mouse.get_pos()
        particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.15
            pygame.draw.circle(WIN, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            radius = particle[2] * 2
            WIN.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)),special_flags=pygame.BLEND_RGB_ADD)

            if particle[2] <= 0:
                particles.remove(particle)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

