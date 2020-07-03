
import pygame
import os
import random
import math
pygame.init()

W, H = 800, 680
WINDOW = pygame.display.set_mode((W, H))
BG = pygame.image.load(os.path.join("assets", "piso2.png"))
player = pygame.image.load(os.path.join("assets", "player.png"))
gameover = False

class Character(pygame.sprite.Sprite):
    def __init__(self, strong, vel, ang_vel, health = 100, angle = 90):
        self.health = health
        self.vel = vel
        self.ang_vel = ang_vel
        self.strong = strong
        self.sheet = None
        self.angle = angle
        self.bullet = None

class Player(Character):
    def __init__(self, strong, vel, ang_vel):
        global W, H
        super().__init__(strong, vel, ang_vel)
        self.sheet = pygame.image.load(os.path.join("assets", "player.png"))
        self.offset = (self.sheet.get_width()/2, self.sheet.get_height()/2)
        self.p_x = 300
        self.p_y = 300


    def anglePlayer(self, degree):
        self.angle += degree
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360

    def walkingPlayer(self, vel):

        self.p_x += math.cos(math.radians(self.angle))*vel
        self.p_y += math.sin(math.radians(self.angle))*vel
        print("angulo:", self.angle, "posX:", self.p_x, "posY:", self.p_y, "mouseX e Y:", "velX:", math.cos(self.angle)*vel, "velY:", math.sin(self.angle)*vel )

    def update(self, keys):
        if keys[pygame.K_RIGHT]:
            self.anglePlayer(self.ang_vel)
        if keys[pygame.K_LEFT]:
            self.anglePlayer(-self.ang_vel)
        if keys[pygame.K_UP]:
            self.walkingPlayer(self.vel)
        if keys[pygame.K_DOWN]:
            self.walkingPlayer(-self.vel)

        img = pygame.transform.rotate(self.sheet, - (self.angle + 90))

        WINDOW.blit(img, (self.p_x - self.offset[0], self.p_y - self.offset[1]))


cursor = pygame.image.load(os.path.join("assets","gunsight.png"))
pygame.mouse.set_visible(False)
player_one = Player(100, 5, 4)
while gameover == False:
    WINDOW.blit(BG,(0,0))
    player_one.update(pygame.key.get_pressed())
    WINDOW.blit(cursor, (pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

