import pygame
from pygame.locals import *
from random import randint
import os
import sys
import math

pygame.init()

W, H = 1500, 800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('side-scroller-game\images','game_background_1.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

VEL = 5
BULLET_VEL = 10
RED = (255, 0, 0)
GREEN = (0,100,0)
ORANGE = (255,165,0)
BG_SPEED = 1.4
bullets = []
class Player(object):
    # run = [pygame.image.load(os.path.join('side-scroller-game\images', str(x) + '.png')) for x in range(8,16)]
    ship = pygame.image.load(os.path.join('side-scroller-game\images', 'transparant_ship.png'))
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
  

    def handle_bullets(self, bullets, enemies):
        for bullet in bullets:
            bullet.x += BULLET_VEL
            # for enemy in enemies:
            # if enemy.colliderect(bullet):
            #     pygame.event.post(pygame.event.Event(enemy_HIT))
            #     bullets.remove(bullet)
            if bullet.x > W:
                bullets.remove(bullet)
    
    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x - VEL > 0:            # left
            self.x -= VEL
        if keys_pressed[pygame.K_d] and self.x + VEL + self.width < W:            # right
            self.x += VEL
        if keys_pressed[pygame.K_w] and self.y - VEL > 0:            # up
            self.y -= VEL
        if keys_pressed[pygame.K_s] and self.y + VEL + self.height < H - 15:            # down
            self.y += VEL

    def draw(self, win, keys_pressed, bullets):
        self.handle_movement(keys_pressed)
        # self.handle_bullets(bullets)

            
        # else:
        #     if self.runCount > 42:
        #         self.runCount = 0
        win.blit(self.ship, (self.x,self.y))
            # self.runCount += 1


class Enemy(object):
    enemy_ship = pygame.image.load(os.path.join('side-scroller-game\images', 'enemy1.png'))
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = W + 50
        self.y = randint(0 + 50, H - 50)
        self.speed = 0
        self.damage = 1
        self.hp = 3
        self.vel = 3
        self.drop = None

    def draw(self, win):
        # self.handle_movement(keys_pressed)
        # self.handle_bullets(bullets)

            
        # else:
        #     if self.runCount > 42:
        #         self.runCount = 0
        win.blit(self.enemy_ship, (self.x,self.y))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
    

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        if self.radius == -1:
            bullet_rect = pygame.Rect(self.x, self.y, 10, 5)
            pygame.draw.rect(win, RED, bullet_rect)
        else:
            pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        # print(bullets)


def redrawWindow(bullets):
    win.blit(bg, (bgX,0))
    win.blit(bg, (bgX2,0))
    keys_pressed = pygame.key.get_pressed()

    player.draw(win, keys_pressed, bullets)
    enemy.draw(win)
    for bullet in bullets:
        # pygame.draw.rect(win, RED, bullet)
        bullet.draw(win)


    pygame.display.update()


player = Player(200, H-100, 64, 64)
enemy = Enemy(81, 69)
pygame.time.set_timer(USEREVENT+1,500)
speed = 80
run = True
previous_time = pygame.time.get_ticks()
while run:
    bgX -= BG_SPEED
    bgX2 -= BG_SPEED
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()    
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():  # Loop through a list of events
        if event.type == pygame.QUIT:  # See if the user clicks the red x 
            run = False    # End the loop
            pygame.quit()  # Quit the game
            quit()
        # if event.type == USEREVENT+1:
        #     speed +=1

        

    current_time = pygame.time.get_ticks()

    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_SPACE]:
        if current_time - previous_time > 150:
            previous_time = current_time
            bullets.append(projectile(round(player.x + player.width/2), round(player.y + player.height/2), 5, ORANGE, 1))
            # bullets.append(projectile(round(player.x + player.width/2), round(player.y + player.height/2), -1, RED, 1))


    for bullet in bullets:
        # if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
        #     if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
        #         goblin.hit()
        #         score += 1
        #         bullets.pop(bullets.index(bullet))
                
        if bullet.x < W and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))            
    
    redrawWindow(bullets)

    clock.tick(speed)

