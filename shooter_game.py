#Создай собственный Шутер!

from pygame import *
import random
win_width = 700
win_height = 500
clock = time.Clock()
FPS = 60
count = 0
died = 0
num_fire = 0
rel_time = False

window = display.set_mode((win_width, win_height))
space = transform.scale(image.load('galaxy.jpg'), (700, 500))
display.set_caption('Fire')
#music
mixer.init()
mixer.music.load('space.ogg') 
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.rect.x-= 5
        if keys_pressed[K_RIGHT]:
            self.rect.x+= 5
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = random.randrange(0, 10)
            self.rect.x = random.randrange(0, 100)
            global count
            count = count + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        
class Astero(GameSprite):
    def update(self):
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = random.randrange(0, 10)
            self.rect.x = random.randrange(0, 100)

#font
font.init()
font = font.SysFont('Arial', 25)

player = Player('rocket.png', 300,430, 2, 65, 65)

mobs = sprite.Group()
bullets = sprite.Group()
asteros = sprite.Group()
for i in range(1,3):
    enemy = Enemy('ufo.png', random.randrange(0, 700), 0, random.randrange(2,4), 65 ,65)
    mobs.add(enemy)
run = True
finish = True
while run:
    fail = font.render(f'Пропущено: {count}', True, (224, 255, 255))
    win = font.render(f'Счёт: {died}', True, (224, 255, 255))
    window.blit(space, (0, 0))
    window.blit(win, (0, 0))
    window.blit(fail, (0, 25))
    for e in event.get():
        if e.type == QUIT:
            run = False
    if e.type == KEYDOWN:
        if e.key == K_w:
            player.fire()
    if finish == True:
        group_list = sprite.groupcollide(mobs, bullets, True, True)
        for s in group_list:
            died += 1
            enemy = Enemy('ufo.png', random.randrange(0, 700), 0, random.randrange(2,4), 65 ,65)
            mobs.add(enemy)
        if died == 10:
            finish = False
            winner = font.render('Победа!', True, (0, 255, 0))
            window.blit(winner, (0, 100))
        if count == 3:
            failure = font.render('Проигрыш!', True, (204, 0, 0))
            window.blit(failure, (0, 100))
            finish = False
        if sprite.spritecollide(player, mobs, False):
            failure = font.render('Проигрыш!', True, (204, 0, 0))
            window.blit(failure, (0, 100))
            finish = False
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)
        mobs.update()
        mobs.draw(window)
        clock.tick(FPS)
        display.update()