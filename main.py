import pygame
import random
import math
from pygame import mixer

# Initilaize pygame
pygame.init()

# Create the display
screen = pygame.display.set_mode((800, 600))

# title, icon and background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ovni.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Fondo.jpg")

# music
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Player Attributes
img_player = pygame.image.load("cohete.png")
player_x = 368
player_y = 500
player_x_change = 0
player_y_change = 0

# Enemies Attributes
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_quantity = 8

for e in range(enemy_quantity):
    img_enemy.append(pygame.image.load("enemigo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.1)
    enemy_y_change.append(50)

# Bullet Attributes
img_bullet = pygame.image.load("bala.png")
bullet_x = 0
bullet_y = 500
bullet_y_change = 1
bullet_visible = False

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Endgame Text
end_font = pygame.font.Font("freesansbold.ttf", 40)

# Function Score
def show_score(x, y):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


# Function Player
def player(x, y):
    screen.blit(img_player, (x, y))


# Function Enemy
def enemy(x, y, ene):
    screen.blit(img_enemy[ene], (x, y))


# Function Bullet
def bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(img_bullet, (x + 16, y + 10))


# Function Collision
def collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False


# Endgame Function
def final_text():
    final_font = end_font.render("GAME ENDED", True, (255, 255, 255))
    screen.blit(final_font, (250,200))


# Game loop
working = True
while working:

    # RGB
    screen.blit(background, (0, 0))

    # Event iteration
    for event in pygame.event.get():
        # Close game
        if event.type == pygame.QUIT:
            working = False

        # Keys pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.2
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.2
            if event.key == pygame.K_SPACE:
                s_bullet = mixer.Sound("disparo.mp3")
                s_bullet.play()
                if not bullet_visible:
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)

        # Keys unpressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_change = 0
            if event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player location
    player_x += player_x_change
    player_y += player_y_change

    # Player limits
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy location
    for e in range(enemy_quantity):

        # endgame
        if enemy_y[e] > 450:
            for k in range(enemy_quantity):
                enemy_y[k] = 1000
            final_text()
            break

        enemy_x[e] += enemy_x_change[e]

        # Enemy limits
        if enemy_x[e] <= 0:
            enemy_x_change[e] = 0.1
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -0.1
            enemy_y[e] += enemy_y_change[e]

        # Collision
        v_collision = collision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if v_collision:
            s_collision = mixer.Sound("Golpe.mp3")
            s_collision.play()
            bullet_y = 500
            bullet_visible = False
            score += 1
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(50, 200)

        enemy(enemy_x[e], enemy_y[e], e)

    # Bullet movement
    if bullet_y <= -64:
        bullet_y = 500
        bullet_visible = False
    if bullet_visible:
        bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)

    show_score(text_x, text_y)

    # Game update
    pygame.display.update()
