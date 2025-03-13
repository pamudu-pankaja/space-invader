import pygame
import random
import math
from pygame import mixer

pygame.init()

# Window Setup
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
WindowIcon = pygame.image.load("pics/icon.png")
WindowBackground = pygame.image.load("pics/background.jpg")
pygame.display.set_icon(WindowIcon)

#Score
score = 0

# Background Music
mixer.music.load("sounds/background_rec.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Player Setup
playerImg = pygame.image.load("pics/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20
            
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("pics/ufo.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet Setup
bulletImg = pygame.image.load("pics/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

font = pygame.font.Font("font/SuperLegendBoy-4w8Y.ttf", 30)

# Game Over Text
def game_over():
    global running

    over_font = pygame.font.Font("font/SuperLegendBoy-4w8Y.ttf", 60)
    option_font = pygame.font.Font("font/SuperLegendBoy-4w8Y.ttf", 25)
    
    gameOver = True
    if gameOver:
        over_text = window.blit(over_font.render("Game Over", False, (255, 215, 0)), (200, 200))
        restart_text = window.blit(option_font.render('Press "Enter" to try again ', False, (255, 215, 0)), (180, 315))
        exit_text = window.blit(option_font.render('Press "Esc" to exit', False, (255, 215, 0)), (240, 355))
        pygame.display.update()
    else :
        False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart game
                    gameOver = False
                    reset_game()
                    return
                if event.key == pygame.K_ESCAPE:  # Exit game
                    pygame.quit()
                    exit()

# Reset Game
def reset_game():
    global score, playerX, bulletY, bullet_state, enemyX, enemyY

    score = 0
    playerX = 370
    bulletY = 480
    bullet_state = "ready"

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)

    game()

#Ending Line
def ending_line():
    font = pygame.font.Font("font/SuperLegendBoy-4w8Y.ttf", 45)
    endingText = window.blit(font.render("______________________", True, (255, 191, 0)), (0, 400))
# Display Score
def display_score():
    score_string = font.render("SCORE : " + str(score), True, (255, 215, 0))
    window.blit(score_string, (10, 10))

# Player Movement
def player(x, y):
    window.blit(playerImg, (x, y))

# Enemy Movement
def enemy(x, y, i):
    window.blit(enemyImg[i], (x, y))

# Fire Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImg, (x + 16, y + 10))

# Collision Detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Main Game Loop
def game():
    global running, playerX, playerX_change, playerY, enemyX, enemyX_change, enemyY, enemyY_change
    global bulletX, bullet_state, bulletY, bulletY_change, score,num_of_enemies

    running = True
    while running:
        window.blit(WindowBackground, (0, 0))
        #window.blit(redLine,(0,200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    playerX_change = 3.5

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    playerX_change = -3.5

                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("sounds/laser.wav")
                        bullet_sound.play()
                        bullet_sound.set_volume(0.15)
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_d, pygame.K_a, pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

        # Player movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(num_of_enemies):
            if enemyY[i] > 200:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over()
                return  # Stop game loop when game over

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1.5
                enemyY[i] += enemyY_change[i]

            # Collision check
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                explosion_sound = mixer.Sound("sounds/explosion.wav")
                explosion_sound.play()
                explosion_sound.set_volume(0.3)
                score += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        ending_line()
        display_score()
        player(playerX, playerY)
        pygame.display.update()

# Start Game
if __name__ == "__main__":
    game()

