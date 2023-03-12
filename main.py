# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from os import path
WIDTH = 1000  # ширина игрового окна
HEIGHT = 500# высота игрового окна
FPS = 60 # частота кадров в секунду  

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
background = pygame.image.load(path.join(img_dir, 'Backgrounds/purple.png')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
player_img = pygame.image.load(path.join(img_dir, "PNG/playerShip1_red.png")).convert()

bullet_img = pygame.image.load(path.join(img_dir, "PNG/Lasers/laserRed05.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Playerlaser.wav'))
shoot_sound.set_volume(0.3)
expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl_sound.mp3'))
expl_sound.set_volume(0.45)
meteor_imgs = []
for num in range(1,20): 
    meteor_imgs.append(pygame.image.load(path.join(img_dir, "PNG/Meteors/meteor" + str(num) + ".png")).convert())

pygame.mixer.music.load(path.join(snd_dir, 'bgsound.ogg'))
pygame.mixer.music.set_volume(0.4)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (100, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 1
        self.speedy = 0
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_imgs)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3,3)
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
          self.last_update = now
          self.rot = (self.rot + self.rot_speed) % 360
          self.image = pygame.transform.rotate(self.image_orig, self.rot)
        # вращение спрайтов
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (20, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()
all_sprites = pygame.sprite.Group()
mobs=pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(13):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Обновление
    hits = pygame.sprite.spritecollide(player, mobs, False)
    #if hits:
       # running = False
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        expl_sound.play()
    all_sprites.update()
    # Визуализация (сборка)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
