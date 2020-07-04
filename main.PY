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
    def __init__(self, x, y, strong, vel, health = 100, angle = 0):
        self.p_x = x
        self.p_y = y
        self.health = health
        self.vel = vel
        self.strong = strong
        self.sheet = None
        self.angle = angle

        self.bulletList = []

    def shoot(self, shooter, vel, hurt, origin, img, angle, angle_pos):
        bullet = Bullet(shooter, vel, hurt, origin, pygame.image.load(os.path.join("assets", img)), angle, angle_pos)
        self.bulletList.append(bullet)

    def bulletsMove(self):
        for bullet in self.bulletList:
            bullet.moveBullet()
            if bullet.off_screen(WINDOW.get_width(), WINDOW.get_height()):
                self.bulletList.remove(bullet)

class Player(Character):
    def __init__(self, x, y, strong, vel):
        super().__init__(x, y, strong, vel)
        self.sheet = pygame.image.load(os.path.join("assets", "player.png"))
        self.mask = pygame.mask.from_surface(self.sheet)
        self.anglePlayer(pygame.mouse.get_pos())

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

    def event(self, keys):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.anglePlayer(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.anglePlayer(pygame.mouse.get_pos())
                self.shoot(self, 8, 10, 33, "bullet1.png", self.angle, 15)
        if keys[pygame.K_w]:
            self.movePlayer("foward")
        if keys[pygame.K_s]:
            self.movePlayer("backward")
        if keys[pygame.K_a]:
            self.movePlayer("left")
        if keys[pygame.K_d]:
            self.movePlayer("right")

        self.bulletsMove()
        img = pygame.transform.rotate(self.sheet, - (self.angle + 90))
        self.offsetcenter = (img.get_width()/2 , img.get_height()/2)
        WINDOW.blit(img, (self.p_x - self.offsetcenter[0], self.p_y - self.offsetcenter[0]))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, shooter, vel, hurt, origin, sheet, angle, angle_pos):
        self.vel = vel
        self.hurt = hurt
        self.origin = origin
        self.angle_pos = angle_pos
        self.angle = angle
        self.sheet = sheet
        self.mask = pygame.mask.from_surface(self.sheet)
        self.angle_origin = self.angle - self.angle_pos
        self.b_x = shooter.p_x
        self.b_y = shooter.p_y
        self.b_x += math.cos(math.radians(self.angle_origin))*self.origin
        self.b_y += math.sin(math.radians(self.angle_origin))*self.origin

    def moveBullet(self):
        self.b_x += math.cos(math.radians(self.angle))*self.vel
        self.b_y += math.sin(math.radians(self.angle))*self.vel
        WINDOW.blit(self.sheet, (self.b_x,self.b_y))
        print("b_x:", self.b_x, "b_y:", self.b_y,"angulo origen:", self.angle_pos + self.angle, "angulo:", self.angle)

    def off_screen(self, width, height):
        return (not(self.b_x <= width and self.b_x >= 0) or not(self.b_y <= height and self.b_y >= 0))



cursor = pygame.image.load(os.path.join("assets","gunsight.png"))
pygame.mouse.set_visible(False)
player_one = Player(300, 400, 100, 7)
while gameover == False:
    WINDOW.blit(BG,(0,0))
    player_one.event(pygame.key.get_pressed())
    WINDOW.blit(cursor, (pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

