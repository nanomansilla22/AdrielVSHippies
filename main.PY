import pygame
import os
import random
import math
pygame.init()

W, H = 800, 680
WINDOW = pygame.display.set_mode((W, H))
BG = pygame.image.load(os.path.join("assets", "piso2.png"))
bullet = pygame.image.load(os.path.join("assets", "bullet1.png"))
gameover = False

class Character(pygame.sprite.Sprite):
    def __init__(self, strong, vel, health = 100, angle = 0):
        self.health = health
        self.vel = vel
        self.strong = strong
        self.sheet = None
        self.angle = angle

class Bullet(pygame.sprite.Sprite):
    def __init__(self, vel, hurt, origin, sheet):
        self.vel = vel
        self.hurt = hurt
        self.origin = origin
        self.sheet = sheet
        self.mask = pygame.mask.from_surface(self.sheet)


    def originShoot(self, angle, angle_pos, x, y):
        self.angle = angle
        if angle > 270 and angle <= 360:
            self.b_x = math.sin(math.radians(angle_pos))*self.origin
            self.b_y = math.cos(math.radians(angle_pos))*self.origin
        if angle > 180 and angle <= 270:
            self.b_x = math.cos(math.radians(angle_pos))*self.origin
            self.b_y = math.sin(math.radians(angle_pos))*self.origin
        if angle > 90 and angle <= 180:
            self.b_x = math.sin(math.radians(angle_pos))*self.origin
            self.b_y = math.cos(math.radians(angle_pos))*self.origin
        if angle > 90 and angle < 0:
            self.b_x = math.cos(math.radians(angle_pos))*self.origin
            self.b_y = math.sin(math.radians(angle_pos))*self.origin

    def draw(self, x, y):
        WINDOW.blit(self.sheet, (self.b_x,self.b_y))



    def move(self):
        self.b_x += math.cos(math.radians(self.angle))*self.vel
        self.b_y += math.sin(math.radians(self.angle))*self.vel

class Player(Character):
    def __init__(self, strong, vel):
        super().__init__(strong, vel)
        self.sheet = pygame.image.load(os.path.join("assets", "player.png"))
        self.mask = pygame.mask.from_surface(self.sheet)
        self.p_x = 300
        self.p_y = 300
        self.anglePlayer(pygame.mouse.get_pos())
        self.bullet = Bullet(8, 10, 35, pygame.image.load(os.path.join("assets","bullet1.png")))


    def anglePlayer(self, mousepos):
        self.m_x, self.m_y = mousepos
        ady = self.m_x - (self.p_x)
        op = self.m_y - (self.p_y)
        hip = math.sqrt(op*op + ady*ady)
        if op > 0:
            self.angle = math.degrees(math.acos(ady/hip))
        elif op <= 0:
            self.angle = 360 - math.degrees(math.acos(ady/hip))


    def movePlayer(self, direction):
        if direction == "foward":
            angle = math.radians(self.angle)
        if direction == "backward":
            angle = math.radians(self.angle + 180)
        if direction == "left":
            angle = math.radians(self.angle - 90)
        if direction == "right":
            angle = math.radians(self.angle + 90)
        self.p_x += math.cos(angle)*self.vel
        self.p_y += math.sin(angle)*self.vel

    def shootPlayer(self):
        self.bullet.update

    def update(self, keys):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.anglePlayer(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                self.shootPlayer()
        if keys[pygame.K_w]:
            self.movePlayer("foward")
        if keys[pygame.K_s]:
            self.movePlayer("backward")
        if keys[pygame.K_a]:
            self.movePlayer("left")
        if keys[pygame.K_d]:
            self.movePlayer("right")

        img = pygame.transform.rotate(self.sheet, - (self.angle + 90))
        print("angulo:", self.angle, "posX:", self.p_x, "posY:", self.p_y)
        self.offsetcenter = (img.get_width()/2 , img.get_height()/2)
        WINDOW.blit(img, (self.p_x - self.offsetcenter[0], self.p_y - self.offsetcenter[0]))


cursor = pygame.image.load(os.path.join("assets","gunsight.png"))
pygame.mouse.set_visible(False)
player_one = Player(100,10)
while gameover == False:
    WINDOW.blit(BG,(0,0))
    player_one.update(pygame.key.get_pressed())
    WINDOW.blit(cursor, (pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16))
    WINDOW.blit(bullet,(300,400))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

