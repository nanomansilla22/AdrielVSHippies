import pygame
import os
import random
from random import randint
import math
pygame.init()

W, H = 800, 680
WINDOW = pygame.display.set_mode((W, H))
BG = pygame.image.load(os.path.join("assets", "piso2.png"))
bullet = pygame.image.load(os.path.join("assets", "bullet1.png"))
gameover = False
clock = pygame.time.Clock()
FPS = 60
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, strong, vel, health = 100, angle = 0):
        self.x = x
        self.y = y
        self.health = health
        self.vel = vel
        self.strong = strong
        self.sheet = None
        self.angle = angle

        self.bulletList = []
        self.cont = 0

    def moveCharacter(self, playerx, playery):
        px, py = playerx, playery
        ady = px - (self.x)
        op = py - (self.y)
        hip = math.sqrt(op*op + ady*ady)
        if op > 0:
            self.angle = math.degrees(math.acos(ady/hip))
        elif op <= 0:
            self.angle = 360 - math.degrees(math.acos(ady/hip))
        self.cont = 0

        self.x += math.cos(math.radians(self.angle))*self.vel
        self.y += math.sin(math.radians(self.angle))*self.vel

    def update(self):
        img = pygame.transform.rotate(self.sheet, - (self.angle + 90))
        self.offsetcenter = (img.get_width()/2 , img.get_height()/2)
        WINDOW.blit(img, (self.x - self.offsetcenter[0], self.y - self.offsetcenter[0]))

    def shoot(self, shooter, vel, hurt, origin, img, angle, angle_pos):
        bullet = Bullet(shooter, vel, hurt, origin, pygame.image.load(os.path.join("assets", img)), angle, angle_pos)
        self.bulletList.append(bullet)

    def bulletsMove(self, objs):
        for bullet in self.bulletList:
            if bullet.moveBullet(objs):
                self.bulletList.remove(bullet)
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
        ady = self.m_x - (self.x)
        op = self.m_y - (self.y)
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
        self.x += math.cos(angle)*self.vel
        self.y += math.sin(angle)*self.vel

    def update(self, keys, objs):
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

        self.bulletsMove(objs)
        img = pygame.transform.rotate(self.sheet, - (self.angle + 90))
        self.offsetcenter = (img.get_width()/2 , img.get_height()/2)
        WINDOW.blit(img, (self.x - self.offsetcenter[0], self.y - self.offsetcenter[0]))

class Hippies(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 2, 60, random.randint(0, 360))
        self.sheet = pygame.image.load(os.path.join("assets", "player.png"))
        self.mask = pygame.mask.from_surface(self.sheet)
        self.delay_movement = 10

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
        self.x = shooter.x
        self.y = shooter.y
        self.x += math.cos(math.radians(self.angle_origin))*self.origin
        self.y += math.sin(math.radians(self.angle_origin))*self.origin

    def moveBullet(self, objs):
        self.x += math.cos(math.radians(self.angle))*self.vel
        self.y += math.sin(math.radians(self.angle))*self.vel
        WINDOW.blit(self.sheet, (self.x,self.y))
        for obj in objs:
            if self.collision(obj):
                obj.health -= self.hurt
                print(obj.health)
                deletebullet = True
            else:
                deletebullet = False
            return deletebullet

    def off_screen(self, width, height):
        return (not(self.x <= width and self.x >= 0) or not(self.y <= height and self.y >= 0))

    def collision(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj2.offsetcenter[0] - obj1.x)
    offset_y = int(obj2.y - obj2.offsetcenter[1] - obj1.y)
    ad = obj1.mask.overlap(obj2.mask, (offset_x, offset_y))
    return ad != None

cursor = pygame.image.load(os.path.join("assets","gunsight.png"))
pygame.mouse.set_visible(False)
player_one = Player(300, 400, 100, 7)
enemiesList = []
hippie = Hippies(600,400)
enemiesList.append(hippie)

while gameover == False:
    clock.tick(FPS)
    WINDOW.blit(BG,(0,0))
    player_one.update(pygame.key.get_pressed(), enemiesList)
    for enemy in enemiesList:
        if enemy.health <= 0:
            enemiesList.remove(enemy)
        else:
            #enemy.moveCharacter(player_one.x, player_one.y)
            enemy.update()

            if collide(enemy, player_one):
                    player_one.health -= 1
                    print(player_one.health)

    WINDOW.blit(cursor, (pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

