import pygame
from pygame.locals import *
from random import randint
import os
import sys
import math
import time

pygame.init()

W, H = 1500, 800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('scroller-game\images','game_background_1.png')).convert()
bgX = 0
bgX2 = bg.get_width()
clock = pygame.time.Clock()

VEL = 8
BULLET_VEL_PLAYER = 13
BULLET_VEL_ENEMY = 6
BG_SPEED = 2
RELOAD = 500
SPAWN_COOLDOWN = 2000
NO_ENEMIES = 3

RED = (255, 0, 0)
GREEN = (0,100,0)
ORANGE = (255,105,0)

bullets = []

#-------------------------------  player  -------------------------------#
#------------------------------------------------------------------------#
class Player(object):
    # run = [pygame.image.load(os.path.join('side-scroller-game\images', str(x) + '.png')) for x in range(8,16)]
    ship = pygame.image.load(os.path.join('scroller-game\images', 'transparant_ship.png'))
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.max_hp = 5
        self.hp = self.max_hp
        self.width = width
        self.height = height
        self.hitbox = (self.x , self.y, self.width, self.height)

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.x - VEL > 0:            # left
            self.x -= VEL
        if keys_pressed[pygame.K_d] and self.x + VEL + self.width < W:            # right
            self.x += VEL
        if keys_pressed[pygame.K_w] and self.y - VEL > 0:            # up
            self.y -= VEL
        if keys_pressed[pygame.K_s] and self.y + VEL + self.height < H - 15:            # down
            self.y += VEL
        self.hitbox = (self.x , self.y, self.width, self.height)

    def draw(self, win, keys_pressed):
        self.handle_movement(keys_pressed)
        win.blit(self.ship, (self.x,self.y))
        self.healthbar(win)
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    
    def hit(self):
        if self.hp > 0:
            self.hp -= 1
    
    def healthbar(self, win):
        pygame.draw.rect(win, (255,0,0), (W/2 - 50, H-12, 100, 10))
        pygame.draw.rect(win, (0,255,0), (W/2 - 50, H-12, 100 * (self.hp/self.max_hp), 10))


#-------------------------------   enemy   -------------------------------#
#-------------------------------------------------------------------------#
class Enemy(object):
    enemy_ship = pygame.image.load(os.path.join('scroller-game\images', 'enemy1.png'))
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = W - 100
        self.y = randint(0 + 100, H - 250)
        self.speed = 0
        self.damage = 1
        self.hp = 1
        self.vel = 2
        self.drop = None
        self.hitbox = (self.x , self.y, self.width, self.height)
        self.visible = True
        self.x_end = W - 100
        self.y_end = H - 100
        self.path = [self.x, self.y, self.x_end, self.y_end]

    def draw(self, win):        
        if self.visible:
            self.move()
            win.blit(self.enemy_ship, (self.x,self.y))
            self.hitbox = (self.x , self.y, self.width, 36)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.y + self.vel < self.path[3]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                
        else:
            if self.y - self.vel > self.path[1]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                
    def hit(self):
        if self.hp > 0:
            self.hp -= 1
        if self.hp <= 0:
            self.visible = False


#------------------------------- projectile -------------------------------#
#--------------------------------------------------------------------------#
class projectile(object):
    def __init__(self, x, y, radius, color, facing, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = velocity * facing
        self.damage = 1
        
    def draw(self,win):
        if self.radius == -1:
            bullet_rect = pygame.Rect(self.x, self.y, 10, 5)
            pygame.draw.rect(win, RED, bullet_rect)
        else:
            pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
#--------------------------------------------------------------------------#

def spawn():
    pass

def redrawWindow(bullets):
    win.blit(bg, (bgX,0))
    win.blit(bg, (bgX2,0))
    keys_pressed = pygame.key.get_pressed()
    player.draw(win, keys_pressed)
    for enemy in enemies:
        enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()



enemies = None
player = Player(200, H-100, 64, 64)
pygame.time.set_timer(USEREVENT+1,500)
speed = 60
run = True
previous_time = pygame.time.get_ticks()
enemy_kill = pygame.time.get_ticks()
prev_time = pygame.time.get_ticks()
title_font = pygame.font.SysFont("comicsans", 70)
instructions_font = pygame.font.SysFont("comicsans", 40)
run = True

#------------------------------- menu screen -------------------------------#
while run:
    win.blit(bg, (0,0))
    title_label = title_font.render("Press the mouse to begin", 1, (255,255,255))
    instructions_label = instructions_font.render("SPACE to shoot, WASD to move", 1, (255,255,255))
    win.blit(title_label, (W/2 - title_label.get_width()/2, 100))
    win.blit(instructions_label, (W/2 - instructions_label.get_width()/2, 170))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #------------------------------- main loop -------------------------------#
            while run:    
                clock.tick(speed)
                              
                bgX -= BG_SPEED
                bgX2 -= BG_SPEED
                if bgX < bg.get_width() * -1:
                    bgX = bg.get_width()    
                if bgX2 < bg.get_width() * -1:
                    bgX2 = bg.get_width()

                if enemies is None:
                    enemies = []
                    for i in range(NO_ENEMIES):                        
                        enemy = Enemy(50, 36)
                        enemies.append(enemy)
                
                for event in pygame.event.get():  
                    if event.type == pygame.QUIT:  
                        run = False    
                        pygame.quit()  
                        quit()
            
                current_time = pygame.time.get_ticks()
                keys_pressed = pygame.key.get_pressed()
                
                #deal with player shooting
                if keys_pressed[pygame.K_SPACE]:
                    if current_time - previous_time > 150:
                        previous_time = current_time
                        bullets.append(projectile(round(player.x + player.width/2 + 35), round(player.y + player.height/2), -1, RED, 1, BULLET_VEL_PLAYER))

                reload_time = pygame.time.get_ticks()
                
                for enemy in enemies:
                    #enemy shoot if player in sights
                    if abs(enemy.y - player.y) < 30 and enemy.visible and reload_time - prev_time > RELOAD:
                        prev_time = reload_time
                        bullets.append(projectile(round(enemy.x + enemy.width/2 - 25), round(enemy.y + enemy.height/2), 5, ORANGE, -1, BULLET_VEL_ENEMY))

                    for bullet in bullets:
                        #check if enemy hit
                        if enemy.visible:
                            if bullet.y < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y > enemy.hitbox[1]:
                                if bullet.x > enemy.hitbox[0] and bullet.x < enemy.hitbox[0] + enemy.hitbox[2]:
                                    bullets.pop(bullets.index(bullet))
                                    enemy.hit()
                        #remove enemy from game if invisible (hp is 0)
                        elif enemy in enemies:      
                            enemies.pop(enemies.index(enemy))
                            enemy_kill = pygame.time.get_ticks()      

                        #check if player hit
                        if bullet.y < player.hitbox[1] + player.hitbox[3] and bullet.y > player.hitbox[1]:
                                if bullet.x > player.hitbox[0] and bullet.x < player.hitbox[0] + player.hitbox[2]:
                                    bullets.pop(bullets.index(bullet))
                                    player.hit()

                #Game over
                if player.hp <= 0:
                    win.blit(bg, (bgX,0))
                    win.blit(bg, (bgX2,0))
                    pygame.display.update()
                    title_label = title_font.render("Game Over... Don't Get Hit LOL", 1, (255,255,255))
                    win.blit(title_label, (W/2 - title_label.get_width()/2, 350))
                    pygame.display.update()
                    time.sleep(3)
                    quit()

                for bullet in bullets:
                    #move bullets & remove bullet if goes off screen        
                    if bullet.x < W and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        bullets.pop(bullets.index(bullet))                

                if len(enemies) < 3 and pygame.time.get_ticks() - enemy_kill > SPAWN_COOLDOWN:
                    enemy = Enemy(50, 36)
                    enemies.append(enemy)
                redrawWindow(bullets)
