import pygame
import random
import sys
import os
import math
import pytweening

### SIMPLE FALLING BRICK GAME WITH BLACK METAL PERSONAS ###

# ASSETS

# using os will make sure that file paths will be accessed by most computers
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
aud_folder = os.path.join(game_folder, "audio")
scoreCard = pygame.image.load(os.path.join(img_folder, 'scoreHolder1.png'))
goScreen = pygame.image.load(os.path.join(img_folder, "vargSmiling.jpg"))


# variables
scWIDTH = 1024
scHEIGHT = 820
FPS = 30
speed = 5
playerHolder = scHEIGHT - 90
size = 25
countScore = 0


# colors
shade = (205, 10, 25)
black = (0, 0, 0)

# CLASSES


class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, "euro90.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (scWIDTH / 2, scWIDTH - 45)

    def update(self):
        player.rect.center = pygame.mouse.get_pos()
        if self.rect.right > scWIDTH:
            self.rect.right = scWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < playerHolder:
            self.rect.top = playerHolder


class enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, "varg90.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(45, scWIDTH - 45), -90)
        self.enemySpeed = random.randint(1, 7)

    def update(self):
        self.rect.y += self.enemySpeed
        if self.rect.top > scHEIGHT + 5:
            self.rect.center = (random.randint(45, scWIDTH - 45), -45)
            self.enemySpeed = random.randint(1, 5)
            global countScore
            countScore += 6


class knife(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(
            img_folder, "vargIcon.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(45, scWIDTH - 45), -90)
        self.enemySpeed = 6

    def update(self):
        self.rect.y += self.enemySpeed
        if self.rect.top > scHEIGHT + 5:
            self.rect.center = (random.randint(45, scWIDTH - 45), -45)
            global countScore
            countScore += 6

# Collision Effects


# Scoring
fontName = pygame.font.match_font("arial")


def drawScore(surf, text, size, x, y):
    font = pygame.font.Font(fontName, size)
    textScore = font.render(text, True, shade)
    text_rect = textScore.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(textScore, text_rect)

# TODO
# for every enemy pass + time add point
# higher the points, more vargs appear, faster they travel

# kitchen knife
# if points random number between (certain point range)

# play video/music


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((scWIDTH, scHEIGHT))  # = a tuple
iconImg = pygame.image.load(os.path.join(img_folder, "vargIcon.jpg"))
pygame.display.set_icon(iconImg)
pygame.display.set_caption("Varg VS. Euronymus")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# game initialization
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = player()
enemies = enemy()
knife = knife()
all_sprites.add(player)
for i in range(8):  # this works but will need to iterate
    m = enemy()
    all_sprites.add(m)
    mobs.add(m)

print(os.path.join(aud_folder,'Mysteriis.wav'))
pygame.mixer.music.load(os.path.join(aud_folder,'Mysteriis.ogg'))
pygame.mixer.music.play()
###GAME LOOP###
GAME_OVER = False
caughtKnife = False
knifeCreated = False
while not GAME_OVER:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # update
    screen.fill(black)

    drawScore(screen, str(countScore), 35, scWIDTH - 500, scHEIGHT - 800)
    all_sprites.update()

    # check if player hit
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        GAME_OVER = True

    if countScore > 30 and not knifeCreated:
        all_sprites.add(knife)
        knifeCreated = True

    # Draw/Render
    all_sprites.draw(screen)
    mobs.draw(screen)
    screen.blit(scoreCard, (-65, 1))

    pygame.display.flip()

pygame.mixer.music.stop()
for x in range(100):
    screen.fill(black)
    screen.blit(goScreen, (scWIDTH - (pytweening.easeInCirc(x/99)*scWIDTH), 0))
    pygame.time.delay(50)
    pygame.display.flip()

pygame.time.delay(1500)
