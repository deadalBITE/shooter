from pygame import *
from random import randint
from time import time as tm
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, heigh, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,width))
        self.width = width
        self.heigh = heigh
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > -1:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < xL - 60:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            global rel
            if rel != True:
                mix = mixer.Sound('fire.ogg')
                mix.play()
                global num_fire
                num_fire += 1
                self.fire()
    def fire(self):
        bullet_el = Bullet('bullet.png',self.rect.centerx,self.rect.top,10,10,10)
        bullet_gl.add(bullet_el)
class Enemy(GameSprite):
    def update(self):
        self.direction = 'down'
        self.speed = randint(2, 6)
        if self.direction == 'down':
            self.rect.y += self.speed
        if self.rect.y >= 475:
            self.rect.y = 0
            global n
            n += 1
            self.rect.x = randint(0, 650)
class Enemy1(GameSprite):
    def update(self):
        self.direction = 'down'
        self.speed = randint(6, 10)
        if self.direction == 'down':
            self.rect.y += self.speed
        if self.rect.y >= 475:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
class Bullet(GameSprite):
    def update(self):
        self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= self.speed
def value_gl_ol():
    sprites_list = sprite.groupcollide(monster_gl, bullet_gl, True, True)
    for i in sprites_list:
        global nv
        nv += 1
        monster_cn_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
        monster_gl.add(monster_cn_el)


#ol - подписка на событие
#el - движимый спрайт
#il - недвижимый спрайт
#gl - групповой спрайт
num_fire = 0
rel_tm = 0
rel = False
win_il = font.Font(None,70)
lose_il = font.Font(None,70)
finish = True
xL = 700
yL = 500
n = 0
nv = 0
game = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
window = display.set_mode((xL, yL))
display.set_caption('SHOOTER (Soon)')
monster_c1_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
monster_c2_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
monster_c3_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
monster_c4_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
monster_c5_el = Enemy('ufo.png',randint(0, 650),0,50,50,10)
monster_cE1_el = Enemy1('asteroid.png',randint(0, 650),0,50,50,10)
monster_cE2_el = Enemy1('asteroid.png',randint(0, 650),0,50,50,10)
monster_cE3_el = Enemy1('asteroid.png',randint(0, 650),0,50,50,10)
bullet_gl = sprite.Group()
monster_gl = sprite.Group()
monsterEV_gl = sprite.Group()
monster_gl.add(monster_c1_el)
monster_gl.add(monster_c2_el)
monster_gl.add(monster_c3_el)
monster_gl.add(monster_c4_el)
monster_gl.add(monster_c5_el)
monsterEV_gl.add(monster_cE1_el)
monsterEV_gl.add(monster_cE2_el)
monsterEV_gl.add(monster_cE3_el)
sprite1_el = Player('rocket.png',350,450,50,50,10)
background_il = transform.scale(image.load('galaxy.jpg'), (xL, yL))
font.init()
text1 = font.Font(None, 50).render('Счёт: ' + str(nv), True, (255,255,255))
text2 = font.Font(None, 50).render('Пропущено: ' + str(n), True, (255,255,255))
clock = time.Clock()
FPS = 30 
while game:
    if finish == True:
        window.blit(background_il, (0,0))
        sprite1_el.reset()
        sprite1_el.update()
        bullet_gl.draw(window)
        monster_gl.draw(window)
        monsterEV_gl.draw(window)
        bullet_gl.update()
        monster_gl.update()
        monsterEV_gl.update()
        window.blit(text1, (0,0))
        text1 = font.Font(None, 50).render('Счёт: ' + str(nv), True, (255,255,255))
        text2 = font.Font(None, 50).render('Пропущено: ' + str(n), True, (255,255,255))
        window.blit(text2, (0,50))
        if rel == True:
            text3 = font.Font(None, 50).render('Перезарядка...', True, (255,255,255))
            window.blit(text3, (230,230))
        value_gl_ol()
        if num_fire > 60:
            rel = True
            num_fire = 0
        if n >= 7:
            lose = lose_il.render('YOU LOSE', True, (255, 0, 0))
            window.blit(lose,(200,250))
            finish = False
        if nv >= 10:
            win = win_il.render('YOU WIN', True, (0, 255, 0))
            window.blit(win,(200,250))
            finish = False
        if sprite.spritecollide(sprite1_el, monster_gl, False) or sprite.spritecollide(sprite1_el, monsterEV_gl, False):
            lose = lose_il.render('YOU LOSE', True, (255, 0, 0))
            window.blit(lose,(200,250))
            finish = False
    if rel_tm >= 180:
        rel = False
    if rel == True:
        rel_tm += 1
    if rel != True:
        rel_tm = 0
    for e in event.get():
        if e.type == QUIT:
            game = False
    clock.tick(FPS)
    display.update()
display.update()