import pygame
import random
import math


# INITIALIZE
pygame.init()
# CREATE THE SCREEN
screen = pygame.display.set_mode((650, 550))

# BACKGROUND
bg = pygame.image.load('background.jpg')
# TITLE AND ICON
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# LEVEL
level = 0
font = pygame.font.Font('freesansbold.ttf', 28)

levelX = 485
levelY = 10


def show_level(x, y):
    sc = font.render("LEVEL : " + str(level), True, (255, 255, 255))
    screen.blit(sc, (x, y))


# SCORE
score = 0
font = pygame.font.Font('freesansbold.ttf', 28)

textX = 10
textY = 10


def show_score(x, y):
    sc = font.render("SCORE : " + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))


# GAME OVER
over = pygame.font.Font('freesansbold.ttf', 65)


def game_over():
    over_display = over.render('GAME OVER :(', True, (255, 0, 0))
    f_sc = font.render("Your Final Score is " + str(score), True, (0, 255, 0))
    screen.blit(f_sc, (184, 320))
    screen.blit(over_display, (85, 250))


# PLAYER
player_img = pygame.image.load('spacecraft.png')
playerX = 275
playerY = 480
changeX = 0.0
changeY = 0.0


def player(x, y):
    screen.blit(player_img, (x, y))


# ENEMY
enemies = [pygame.image.load('monster.png'), pygame.image.load('monster1.png'), pygame.image.load('monster2.png'),
           pygame.image.load('monster3.png')]
enemy_img = []
enemyX = []
enemyY = []
e_changeX = []
e_changeY = []
no = 5
count = 0
for i in range(no):
    enemy_img.append(random.choice(enemies))
    enemyX.append(random.randint(0, 550))
    enemyY.append(random.randint(40, 160))
    e_changeX.append(0.0)
    e_changeY.append(0.0)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# BULLET
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
b_changeX = 0.0
b_changeY = 0.0
bullet_state = False


def bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bullet_img, (x + 16, y + 10))


def isShot(x, y, x1, y1):
    dist = math.sqrt(((x - x1) ** 2) + ((y - y1) ** 2))
    if dist < 27:
        return True
    else:
        return False


def distance(x, y, x1, y1):
    dist = math.sqrt(((x - x1) ** 2) + ((y - y1) ** 2))
    return dist


# GAME LOOP
running = True
getout = False
rev = []
while running:

    # BACKGROUND
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # CHECKING KEYSTROKE
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and changeY > -75:
            changeY -= 2
        if event.key == pygame.K_DOWN and changeY < 0:
            changeY += 2
        if event.key == pygame.K_LEFT and changeX > -255:
            changeX -= 2
        if event.key == pygame.K_RIGHT and changeX < 350:
            changeX += 2
        if event.key == pygame.K_SPACE:
            if bullet_state == False:
                bulletX = playerX + changeX
                bullet(bulletX, bulletY)
    player(playerX + changeX, playerY + changeY)

    for i in range(no):
        if distance(enemyX[i] + e_changeX[i], enemyY[i] + e_changeY[i], playerX + changeX, playerY + changeY) < 63:
            getout = True
        if getout == True:
            # MOVE OUT ALL ENEMIES
            for j in range(no):
                enemyY[j] = 6000
            playerY = 60000
            game_over()
            break

        rev.append(False)
        if enemyX[i] + e_changeX[i] < 580 and rev[i] == False:
            e_changeX[i] += 1.5 + level
        else:
            rev[i] = True

        if enemyX[i] + e_changeX[i] <= 0:
            e_changeY[i] += 30

        if enemyX[i] + e_changeX[i] > 0 and rev[i] == True:
            e_changeX[i] -= 1.5 + level
        else:
            rev[i] = False

        if enemyX[i] + e_changeX[i] >= 580:
            e_changeY[i] += 30

        shot = isShot(bulletX, bulletY + b_changeY, enemyX[i] + e_changeX[i], enemyY[i] + e_changeY[i])
        if shot:
            b_changeY = 0
            bullet_state = False
            score += 1
            e_changeX[i] = 0
            e_changeY[i] = 0
            enemy_img.pop(i)
            enemy_img.insert(i, random.choice(enemies))
            enemyX[i] = random.randint(0, 550)
            enemyY[i] = random.randint(40, 160)
            if score == 10:
                level += 1
                break
            elif score > 10 and score % 10 == 0:
                level += 1
                break
        # game_over()
        show_score(textX, textY)
        show_level(levelX, levelY)
        enemy(enemyX[i] + e_changeX[i], enemyY[i] + e_changeY[i], i)

    if bulletY + b_changeY < 0:
        b_changeY = 0
        bullet_state = False
    if bullet_state == True:
        bullet(bulletX, bulletY + b_changeY + changeY)
        b_changeY -= 6.5

    if level - count > 0:
        enemy_img.append(random.choice(enemies))
        enemyX.append(0)
        enemyY.append(0)
        e_changeX.append(0)
        e_changeY.append(0)
        no += 1
        count += 1

    pygame.display.update()
