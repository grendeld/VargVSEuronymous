import pygame
import random
import sys
import os
import math
import pytweening

### SIMPLE FALLING BRICK GAME WITH BLACK METAL PERSONAS ###

# ASSETS

game_folder = os.path.dirname(__file__)
    # using os will make sure that file paths will be accessed by most computers
img_folder = os.path.join(game_folder, "img")
aud_folder = os.path.join(game_folder, "audio")
scoreCard = pygame.image.load(os.path.join(img_folder, 'scoreHolder1.png'))
playerBullet = pygame.image.load(os.path.join(img_folder, 'playerBullet.png'))
explosionFire = pygame.image.load(os.path.join(img_folder, 'explosionFire.jpg'))
gameOverScreen = pygame.image.load(os.path.join(img_folder, "vargSmiling.jpg"))
bg_image = pygame.image.load(os.path.join(img_folder, "darkcastle.jpg"))


# variables
screenWIDTH = 1024
screenHEIGHT = 780
FPS = 30
speed = 5
playerHolder = screenHEIGHT - 90
size = 25
countScore = 0
gameOverText = "Game Over"


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
        self.rect.center = (screenWIDTH / 2, screenWIDTH - 45)

    def update(self):
        player.rect.center = pygame.mouse.get_pos()
        if self.rect.right > screenWIDTH:
            self.rect.right = screenWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < playerHolder:
            self.rect.top = playerHolder

    def shoot(self):
        bullet = Bullet(self.rect.centerx +15, self.rect.top + 125)
        all_sprites.add(bullet)
        bullets.add(bullet)


class enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, "varg90.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(45, screenWIDTH - 45), -90)
        self.enemySpeed = random.randint(1, 7)

    def update(self):
        self.rect.y += self.enemySpeed
        if self.rect.top > screenHEIGHT + 5:
            self.rect.center = (random.randint(45, screenWIDTH - 45), -45)
            self.enemySpeed = random.randint(1, 5)
            global countScore
            countScore += 6



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerBullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill


class knife(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(
            img_folder, "vargIcon.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(45, screenWIDTH - 45), -90)
        self.enemySpeed = 6

    def update(self):
        self.rect.y += self.enemySpeed
        if self.rect.top > screenHEIGHT + 4: #make knife not overlap with other sprites
            self.rect.center = (random.randint(45, screenWIDTH - 45), -45)
            self.enemySpeed = 3
            '''global countScore
            countScore += 6'''


# Scoring
fontName = pygame.font.match_font("Estrangelo Edessa,courier new,arial")


def drawScore(surf, text, size, x, y):
    font = pygame.font.Font(fontName, size)
    textScore = font.render(text, True, shade)
    text_rect = textScore.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(textScore, text_rect)

def drawGameOver(GOsurf, GOtext, GOsize, GOx, GOy):
    fontGO = pygame.font.Font(fontName,GOsize)
    textGO = fontGO.render(GOtext,True, shade)
    textGO_rect = textGO.get_rect()
    textGO_rect.midtop = (GOx, GOy)
    GOsurf.blit(textGO,textGO_rect)
# TODO
# for every enemy pass + time add point
# higher the points, more vargs appear, faster they travel

# kitchen knife
# if points random number between (certain point range)


# play video/music


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screenWIDTH, screenHEIGHT))
iconImg = pygame.image.load(os.path.join(img_folder, "vargIcon.jpg"))
pygame.display.set_icon(iconImg)
pygame.display.set_caption("Varg VS. Euronymus")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# game initialization
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = player()
#what was enemies for????? ↓↓
#enemies = enemy()
knife = knife()
all_sprites.add(player)
for i in range(8):  # this works but will need to iterate
    m = enemy()
    all_sprites.add(m)
    mobs.add(m)

print(os.path.join(aud_folder, 'Mysteriis.wav'))
pygame.mixer.music.load(os.path.join(aud_folder, 'Mysteriis.ogg'))
pygame.mixer.music.play(loops = -1)

###GAME LOOP###
GAME_OVER = False
caughtKnife = False
knifeCreated = False
while not GAME_OVER:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update
    screen.fill(black)
    screen.blit(bg_image, (0,0))


    all_sprites.update()

    # COLLISIONS
    # check if player hit
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        drawGameOver(screen, str(gameOverText),66, screenWIDTH/2, screenHEIGHT/2)
        GAME_OVER = True

    bulletHits = pygame.sprite.groupcollide(bullets,mobs, True, True)
    if bulletHits:
        countScore += 6
        m = enemy()
        all_sprites.add(m)
        mobs.add(m)

    if countScore > 663 and not knifeCreated:
        all_sprites.add(knife)
        knifeCreated = True

    # Draw/Render
    all_sprites.draw(screen)
    mobs.draw(screen)
    screen.blit(scoreCard, (-65, 1))
    drawScore(screen, str(countScore), 35, screenWIDTH - 470, screenHEIGHT - 770)

    pygame.display.flip()




pygame.mixer.music.stop()

pygame.time.delay(4000)

for x in range(100):
    screen.fill(black)
    screen.blit(
        gameOverScreen, (screenWIDTH - (pytweening.easeInCirc(x / 99) * screenWIDTH), 0))
    pygame.time.delay(50)
    pygame.display.flip()

pygame.time.delay(1500)
