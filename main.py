import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

#Pealkiri, logo
pygame.display.set_caption("Mäng")
icon = pygame.image.load('ikooon.png')
pygame.display.set_icon(icon)


# Mängija
mangijapilt = pygame.image.load('mesimumm.png')
mangijaX = 370
mangijaY = 520
mangijaX_muutus = 0

# Vastane
vastasepilt = []
vastaneX = []
vastaneY = []
vastaneX_muutus = []
vastaneY_muutus = []
vastane_nr = 6

for i in range(vastane_nr):
    vastasepilt.append(pygame.image.load('karu.png'))
    vastaneX.append(random.randint(0, 734))
    vastaneY.append(random.randint(0, 50))
    vastaneX_muutus.append(0.1)
    vastaneY_muutus.append(40)

# Mesi
mesipilt = pygame.image.load('mesi.png')
mesiX = 0
mesiY = 480
mesiX_muutus = 0
mesiY_muutus = 0.3
mesi_state = "ready"
# ready - pole ekraanil
#fire - liigub

#Score
score_value = 0
font = pygame.font.SysFont('freesansbold.ttf', 32)

textX = 10
testY = 10

#Game over
over_font = pygame.font.SysFont('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def mangija(x, y):
    screen.blit(mangijapilt, (x, y))


def vastane(x, y, i):
    screen.blit(vastasepilt[i], (x, y))


def fire_mesi(x, y):
    global mesi_state
    mesi_state = "fire"
    screen.blit(mesipilt, (x + 16, y + 10))


def isCollision(vastaneX, vastaneY, mesiX, mesiY):
    kaugus = math.sqrt(math.pow(vastaneX - mesiX, 2) +
                       (math.pow(vastaneY - mesiY, 2)))
    if kaugus < 27:
        return True
    else:
        return False


# Mängu tsükkel
running = True
while running:

    # Taustavärv
    screen.fill((255, 170, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #Mängija liikumine
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mangijaX_muutus = -0.2

            if event.key == pygame.K_RIGHT:
                mangijaX_muutus = 0.2

            if event.key == pygame.K_SPACE:
                if mesi_state == "ready":
                    mesiX = mangijaX
                    fire_mesi(mesiX, mesiY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                mangijaX_muutus = 0

    #Mängija ääred
    mangijaX += mangijaX_muutus

    if mangijaX <= 0:
        mangijaX = 0
    elif mangijaX >= 735:
        mangijaX = 735

    # Vastase liikumine
    for i in range(vastane_nr):

        #Game over
        if vastaneY[i] > 540:
            for j in range(vastane_nr):
                vastaneY[j] = 2000
                game_over_text()
                break

        vastaneX[i] += vastaneX_muutus[i]
        if vastaneX[i] <= 0:
            vastaneX_muutus[i] = 0.15
            vastaneY[i] += vastaneY_muutus[i]
        elif vastaneX[i] >= 735:
            vastaneX_muutus[i] = -0.15
            vastaneY[i] += vastaneY_muutus[i]

        # Collision
        collision = isCollision(vastaneX[i], vastaneY[i], mesiX, mesiY)
        if collision:
            mesiY = 480
            mesi_state = "ready"
            score_value += 1

            vastaneX[i] = random.randint(0, 800)
            vastaneY[i] = random.randint(0, 50)

        vastane(vastaneX[i], vastaneY[i], i)

    # Mee liikumine
    if mesiY <= 0:
        mesiY = 480
        mesi_state = "ready"

    if mesi_state == "fire":
        fire_mesi(mesiX, mesiY)
        mesiY -= mesiY_muutus

    mangija(mangijaX, mangijaY)
    show_score(textX, testY)
    pygame.display.update()
